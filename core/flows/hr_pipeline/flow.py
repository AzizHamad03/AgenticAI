"""HR screening pipeline supporting raw-input and database-driven modes."""

import json
import logging

from typing import List, Optional

from crewai.flow import Flow, listen, start
from django.db import transaction

from core.crews import (
    InterviewQuestionCrew,
    ResumeScreeningCrew,
)

from core.models import (
    Candidate,
    JobPosition,
    Resume,
)

from core.services import (
    InterviewService,
    ScreeningService,
    extract_resume_text,
)

from core.utils import parse_json_output

from .schema import HRPipelineState


logger = logging.getLogger(__name__)


class HRPipelineError(ValueError):
    """
    Human-readable error raised when the pipeline
    cannot be started or completed.
    """
    pass


class HRPipelineFlow(Flow[HRPipelineState]):

    # =========================================================
    # AGENT 1
    # =========================================================

    @start()
    async def screen_resume(self):

        logger.info("Starting resume screening agent...")

        crew = ResumeScreeningCrew().crew()

        result = await crew.kickoff_async(
            inputs={
                "candidate_resume": self.state.candidate_resume,
                "job_title": self.state.job_title,
                "job_description": self.state.job_description,
                "required_skills": self.state.required_skills,
            }
        )

        try:
            self.state.screening_output = parse_json_output(
                result.raw
            )

        except json.JSONDecodeError as exc:

            logger.error(
                "Screening JSON decode error: %s",
                exc,
            )

            self.state.screening_output = {
                "error":
                    "Invalid JSON returned by screening agent"
            }

        return self.state.screening_output

    # =========================================================
    # AGENT 2
    # =========================================================

    @listen(screen_resume)
    async def generate_questions(
        self,
        screening_output,
    ):

        logger.info(
            "Starting interview question agent..."
        )

        crew = InterviewQuestionCrew().crew()

        result = await crew.kickoff_async(
            inputs={
                "candidate_resume":
                    self.state.candidate_resume,

                "job_title":
                    self.state.job_title,

                "job_description":
                    self.state.job_description,

                "screening_report":
                    json.dumps(
                        screening_output,
                        ensure_ascii=False,
                    ),
            }
        )

        try:

            self.state.interview_output = (
                parse_json_output(result.raw)
            )

        except json.JSONDecodeError as exc:

            logger.error(
                "Interview JSON decode error: %s",
                exc,
            )

            self.state.interview_output = {
                "error":
                    "Invalid JSON returned by interview agent"
            }

        return self.state.interview_output

    # =========================================================
    # FINAL RESULT
    # =========================================================

    @listen(generate_questions)
    def combine_results(
        self,
        interview_output,
    ):

        self.state.final_output = {
            "screening_report":
                self.state.screening_output,

            "interview_questions":
                interview_output,
        }

        return self.state.final_output

    # =========================================================
    # DATABASE INPUT LOADING
    # =========================================================

    def _load_database_inputs(
        self,
        candidate_id: int,
        job_position_id: int,
    ) -> None:
        """
        Load everything required by the agents from
        the database.

        IMPORTANT:
        This method is synchronous intentionally.

        Django ORM work happens BEFORE CrewAI starts
        the asynchronous flow steps.
        """

        # -----------------------------------------------------
        # Load Candidate
        # -----------------------------------------------------

        try:

            candidate = Candidate.objects.get(
                pk=candidate_id
            )

        except Candidate.DoesNotExist as exc:

            raise HRPipelineError(
                f"Candidate with id {candidate_id} "
                "was not found."
            ) from exc

        # -----------------------------------------------------
        # Load JobPosition
        # -----------------------------------------------------

        try:

            job_position = JobPosition.objects.get(
                pk=job_position_id
            )

        except JobPosition.DoesNotExist as exc:

            raise HRPipelineError(
                f"Job position with id "
                f"{job_position_id} was not found."
            ) from exc

        # -----------------------------------------------------
        # Find newest resume
        # -----------------------------------------------------

        latest_resume = (
            Resume.objects
            .filter(candidate=candidate)
            .order_by("-uploaded_at")
            .first()
        )

        if latest_resume is None:

            raise HRPipelineError(
                f"Candidate with id {candidate_id} "
                "has no resume on file."
            )

        # -----------------------------------------------------
        # Convert resume file -> plain text
        # -----------------------------------------------------

        try:

            resume_text = extract_resume_text(
                latest_resume.file
            )

        except (OSError, ValueError) as exc:

            raise HRPipelineError(
                f"Could not read the latest resume "
                f"for candidate id {candidate_id}: "
                f"{exc}"
            ) from exc

        if not resume_text:

            raise HRPipelineError(
                "No text could be extracted from "
                f"the latest resume for candidate "
                f"id {candidate_id}."
            )

        # -----------------------------------------------------
        # Populate flow state
        # -----------------------------------------------------

        self.state.candidate_id = candidate.id

        self.state.job_position_id = (
            job_position.id
        )

        self.state.database_mode = True

        self.state.candidate_resume = resume_text

        self.state.job_title = (
            job_position.title
        )

        self.state.job_description = (
            job_position.description or ""
        )

        self.state.required_skills = (
            job_position.required_skills or []
        )

    # =========================================================
    # DATABASE RESULT PERSISTENCE
    # =========================================================

    def _persist_database_results(self) -> None:
        """
        Save the outputs after both AI agents have
        completed.

        This method is also synchronous intentionally.
        """

        # -----------------------------------------------------
        # Ensure screening output is valid
        # -----------------------------------------------------

        if "error" in self.state.screening_output:

            raise HRPipelineError(
                self.state.screening_output["error"]
            )

        # -----------------------------------------------------
        # Ensure interview output is valid
        # -----------------------------------------------------

        if (
            not self.state.interview_output
            or
            "error" in self.state.interview_output
        ):

            message = (
                self.state.interview_output or {}
            ).get(
                "error",
                "Interview agent returned no usable output.",
            )

            raise HRPipelineError(message)

        # -----------------------------------------------------
        # Re-fetch objects from their IDs
        # -----------------------------------------------------

        candidate = Candidate.objects.get(
            pk=self.state.candidate_id
        )

        job_position = JobPosition.objects.get(
            pk=self.state.job_position_id
        )

        # -----------------------------------------------------
        # Save both rows atomically
        # -----------------------------------------------------

        with transaction.atomic():

            screening_result = (
                ScreeningService.create_result(
                    candidate=candidate,
                    job_position=job_position,
                    report=self.state.screening_output,
                )
            )

            question_set = (
                InterviewService.create_question_set(
                    candidate=candidate,
                    job_position=job_position,
                    screening_result=screening_result,
                    questions=self.state.interview_output,
                )
            )

        # -----------------------------------------------------
        # Store generated DB IDs in flow state
        # -----------------------------------------------------

        self.state.screening_result_id = (
            screening_result.id
        )

        self.state.interview_question_set_id = (
            question_set.id
        )

        # Also expose them in the returned JSON.
        self.state.final_output[
            "database_records"
        ] = {
            "screening_result_id":
                screening_result.id,

            "interview_question_set_id":
                question_set.id,
        }

    # =========================================================
    # KICKOFF
    # =========================================================

    def kickoff(
        self,
        candidate_resume: str = "",
        job_title: str = "",
        job_description: str = "",
        required_skills: Optional[List[str]] = None,
        *,
        candidate_id: Optional[int] = None,
        job_position_id: Optional[int] = None,
    ):
        """
        Run the flow in one of two modes.

        DATABASE MODE
        -------------
        Provide:

            candidate_id
            job_position_id

        The resume and job information are automatically
        loaded from the database and the results are saved.

        RAW MODE
        --------
        Do not provide IDs.

        Instead provide:

            candidate_resume
            job_title
            job_description
            required_skills

        Results are NOT saved to the database.
        """

        has_candidate_id = (
            candidate_id is not None
        )

        has_job_id = (
            job_position_id is not None
        )

        # -----------------------------------------------------
        # Prevent passing only one ID
        # -----------------------------------------------------

        if has_candidate_id != has_job_id:

            raise HRPipelineError(
                "Database mode requires both "
                "candidate_id and job_position_id."
            )

        # =====================================================
        # DATABASE MODE
        # =====================================================

        if has_candidate_id and has_job_id:

            self._load_database_inputs(
                candidate_id,
                job_position_id,
            )

        # =====================================================
        # RAW MODE
        # =====================================================

        else:

            self.state.database_mode = False

            self.state.candidate_id = None

            self.state.job_position_id = None

            self.state.candidate_resume = (
                candidate_resume
            )

            self.state.job_title = (
                job_title
            )

            self.state.job_description = (
                job_description
            )

            self.state.required_skills = (
                required_skills or []
            )

        # -----------------------------------------------------
        # Run existing CrewAI flow
        # -----------------------------------------------------

        result = super().kickoff()

        # -----------------------------------------------------
        # Only DB mode saves results
        # -----------------------------------------------------

        if self.state.database_mode:

            self._persist_database_results()

            return self.state.final_output

        # Raw/demo mode returns exactly as before.
        return result