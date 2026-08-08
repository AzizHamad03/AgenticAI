from django.db import models

from .candidate import Candidate
from .job_position import JobPosition
from .screening_result import ScreeningResult


class InterviewQuestionSet(models.Model):
    """
    Structured output produced by the Interview Question Generator (Agent 2).

    Contains technical, behavioral and follow-up questions tailored to the
    candidate, the job and the screening report from Agent 1.
    """

    candidate = models.ForeignKey(
        Candidate,
        on_delete=models.CASCADE,
        related_name="interview_question_sets",
    )
    job_position = models.ForeignKey(
        JobPosition,
        on_delete=models.CASCADE,
        related_name="interview_question_sets",
    )
    # Optional link to the screening result that informed these questions.
    screening_result = models.ForeignKey(
        ScreeningResult,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="interview_question_sets",
    )
    technical_questions = models.JSONField(default=list, blank=True)
    behavioral_questions = models.JSONField(default=list, blank=True)
    follow_up_questions = models.JSONField(default=list, blank=True)
    generated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "interview_question_sets"
        ordering = ["-generated_at"]

    def __str__(self) -> str:
        return f"Questions: {self.candidate.full_name} -> {self.job_position.title}"