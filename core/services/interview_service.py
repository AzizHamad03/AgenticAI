"""Persistence service for interview-question agent output."""

from core.models import InterviewQuestionSet


class InterviewService:

    @staticmethod
    def create_question_set(
        *,
        candidate,
        job_position,
        screening_result,
        questions: dict,
    ) -> InterviewQuestionSet:
        """
        Save the generated interview questions.

        The question set is linked to:
        - Candidate
        - JobPosition
        - ScreeningResult
        """

        return InterviewQuestionSet.objects.create(
            candidate=candidate,
            job_position=job_position,
            screening_result=screening_result,
            technical_questions=questions.get(
                "technical_questions",
                [],
            ),
            behavioral_questions=questions.get(
                "behavioral_questions",
                [],
            ),
            follow_up_questions=questions.get(
                "follow_up_questions",
                [],
            ),
        )