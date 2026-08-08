from django.db import models

from .candidate import Candidate
from .job_position import JobPosition


class ScreeningResult(models.Model):
    """
    Structured output produced by the Resume Screening Agent (Agent 1).

    Stores the match score, extracted strengths/skills and the final
    proceed / hold / reject recommendation for a candidate against a job.
    """

    class Recommendation(models.TextChoices):
        PROCEED = "proceed", "Proceed to Interview"
        HOLD = "hold", "Hold for Review"
        REJECT = "reject", "Reject"

    candidate = models.ForeignKey(
        Candidate,
        on_delete=models.CASCADE,
        related_name="screening_results",
    )
    job_position = models.ForeignKey(
        JobPosition,
        on_delete=models.CASCADE,
        related_name="screening_results",
    )
    # Match score from 0 to 100.
    score = models.FloatField(default=0)
    # JSON lists of strings.
    strengths = models.JSONField(default=list, blank=True)
    missing_skills = models.JSONField(default=list, blank=True)
    recommendation = models.CharField(
        max_length=20,
        choices=Recommendation.choices,
        default=Recommendation.HOLD,
    )
    summary = models.TextField(blank=True)
    # The full, unmodified agent response (useful for debugging / audit).
    raw_report = models.JSONField(default=dict, blank=True)
    generated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "screening_results"
        ordering = ["-generated_at"]

    def __str__(self) -> str:
        return f"Screening: {self.candidate.full_name} -> {self.job_position.title} ({self.score})"