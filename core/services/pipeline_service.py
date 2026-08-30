from core.models import (
    Candidate,
    InterviewQuestionSet,
    JobPosition,
    ScreeningResult,
)


class ResolutionError(ValueError):
    """
    Raised when a candidate or job position
    cannot be resolved.
    """

    pass


class PipelineService:

    # =========================================================
    # CANDIDATE RESOLUTION
    # =========================================================

    @staticmethod
    def resolve_candidate(
        reference,
    ) -> Candidate:

        ref = str(reference).strip()

        if not ref:
            raise ResolutionError(
                "No candidate was provided."
            )

        # Search by ID
        if ref.isdigit():

            try:
                return Candidate.objects.get(
                    pk=int(ref)
                )

            except Candidate.DoesNotExist as exc:
                raise ResolutionError(
                    f"No candidate found with id {ref}."
                ) from exc

        # Search by exact name
        matches = list(
            Candidate.objects.filter(
                full_name__iexact=ref
            )
        )

        # If no exact match, try partial name
        if not matches:

            matches = list(
                Candidate.objects.filter(
                    full_name__icontains=ref
                )
            )

        if not matches:
            raise ResolutionError(
                f"No candidate found matching '{ref}'."
            )

        if len(matches) > 1:

            names = ", ".join(
                f"{candidate.full_name} "
                f"(id {candidate.id})"
                for candidate in matches[:5]
            )

            raise ResolutionError(
                f"Multiple candidates match '{ref}': "
                f"{names}. "
                "Please send the candidate id instead."
            )

        return matches[0]

    # =========================================================
    # JOB RESOLUTION
    # =========================================================

    @staticmethod
    def resolve_job(
        reference,
    ) -> JobPosition:

        ref = str(reference).strip()

        if not ref:
            raise ResolutionError(
                "No job position was provided."
            )

        # Search by ID
        if ref.isdigit():

            try:
                return JobPosition.objects.get(
                    pk=int(ref)
                )

            except JobPosition.DoesNotExist as exc:
                raise ResolutionError(
                    f"No job position found with id {ref}."
                ) from exc

        # Search by exact title
        matches = list(
            JobPosition.objects.filter(
                title__iexact=ref
            )
        )

        # If no exact match, try partial title
        if not matches:

            matches = list(
                JobPosition.objects.filter(
                    title__icontains=ref
                )
            )

        if not matches:
            raise ResolutionError(
                f"No job position found matching '{ref}'."
            )

        if len(matches) > 1:

            titles = ", ".join(
                f"{job.title} (id {job.id})"
                for job in matches[:5]
            )

            raise ResolutionError(
                f"Multiple job positions match '{ref}': "
                f"{titles}. "
                "Please send the job id instead."
            )

        return matches[0]

    # =========================================================
    # RUN PIPELINE
    # =========================================================

    @staticmethod
    def run(
        candidate: Candidate,
        job_position: JobPosition,
    ):

        from core.flows.hr_pipeline.flow import (
            HRPipelineFlow,
        )

        HRPipelineFlow().kickoff(
            candidate_id=candidate.id,
            job_position_id=job_position.id,
        )

        return PipelineService.latest(
            candidate,
            job_position,
        )

    # =========================================================
    # GET LATEST RESULTS
    # =========================================================

    @staticmethod
    def latest(
        candidate: Candidate,
        job_position: JobPosition,
    ):

        screening = (
            ScreeningResult.objects
            .filter(
                candidate=candidate,
                job_position=job_position,
            )
            .order_by("-generated_at")
            .first()
        )

        questions = (
            InterviewQuestionSet.objects
            .filter(
                candidate=candidate,
                job_position=job_position,
            )
            .order_by("-generated_at")
            .first()
        )

        return screening, questions