"""
HR pipeline flow.

Orchestrates the two AI agents in sequence, mirroring the flow-based design of
the reference course project:

    1. Resume Screening Agent  -> produces a screening report.
    2. Interview Question Agent -> uses that report to generate questions.

This flow is used by the `run_pipeline.py` demo script. The REST API endpoints
call the service classes (see `core/services/`) instead, which additionally
persist the results to the database.
"""
import json
import logging

from crewai.flow import Flow, listen, start

from core.crews import InterviewQuestionCrew, ResumeScreeningCrew
from core.utils import parse_json_output

from .schema import HRPipelineState

logger = logging.getLogger(__name__)


class HRPipelineFlow(Flow[HRPipelineState]):

    @start()
    async def screen_resume(self):
        """Step 1: run the Resume Screening Agent."""
        result = await (
            ResumeScreeningCrew()
            .crew()
            .kickoff_async(
                inputs={
                    "candidate_resume": self.state.candidate_resume,
                    "job_title": self.state.job_title,
                    "job_description": self.state.job_description,
                    "required_skills": self.state.required_skills,
                }
            )
        )
        try:
            self.state.screening_output = parse_json_output(result.raw)
        except json.JSONDecodeError as exc:
            logger.error("Screening JSON decode error: %s", exc)
            self.state.screening_output = {"error": "Invalid JSON returned by screening agent"}
        return self.state.screening_output

    @listen(screen_resume)
    async def generate_questions(self):
        """Step 2: run the Interview Question Agent using the screening report."""
        result = await (
            InterviewQuestionCrew()
            .crew()
            .kickoff_async(
                inputs={
                    "candidate_resume": self.state.candidate_resume,
                    "job_title": self.state.job_title,
                    "job_description": self.state.job_description,
                    "screening_report": json.dumps(self.state.screening_output),
                }
            )
        )
        try:
            self.state.interview_output = parse_json_output(result.raw)
        except json.JSONDecodeError as exc:
            logger.error("Interview JSON decode error: %s", exc)
            self.state.interview_output = {"error": "Invalid JSON returned by interview agent"}
        return self.state.interview_output

    @listen(generate_questions)
    def combine_results(self):
        """Step 3: assemble the final combined result."""
        self.state.final_output = {
            "screening_report": self.state.screening_output,
            "interview_questions": self.state.interview_output,
        }
        return self.state.final_output

    def kickoff(
        self,
        candidate_resume: str = "",
        job_title: str = "",
        job_description: str = "",
        required_skills: str = "",
    ):
        """Convenience wrapper so callers can pass inputs positionally."""
        self.state.candidate_resume = candidate_resume
        self.state.job_title = job_title
        self.state.job_description = job_description
        self.state.required_skills = required_skills
        return super().kickoff()