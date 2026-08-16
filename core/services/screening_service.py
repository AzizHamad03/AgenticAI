"""Persistence service for resume-screening agent output."""

from core.models import ScreeningResult


class ScreeningService:

    @staticmethod
    def create_result(
        *,
        candidate,
        job_position,
        report: dict,
    ) -> ScreeningResult:
        """
        Create and save a ScreeningResult from
        the resume-screening agent output.
        """

        return ScreeningResult.objects.create(
            candidate=candidate,
            job_position=job_position,
            score=report.get("match_score", 0),
            strengths=report.get("strengths", []),
            missing_skills=report.get("missing_skills", []),
            recommendation=report.get(
                "hiring_recommendation",
                "hold",
            ),
            summary=report.get("summary", ""),
            raw_report=report,
        )