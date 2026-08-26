from .candidate_create import CandidateCreateAPIView
from .interview_question_set_detail import InterviewQuestionSetDetailAPIView
from .job_position_create import JobPositionCreateAPIView
from .resume_upload import ResumeUploadAPIView
from .screening_result_detail import ScreeningResultDetailAPIView
from .whatsapp import TwilioWhatsAppWebhookView
__all__ = [
    "CandidateCreateAPIView",
    "InterviewQuestionSetDetailAPIView",
    "JobPositionCreateAPIView",
    "ResumeUploadAPIView",
    "ScreeningResultDetailAPIView",
    "TwilioWhatsAppWebhookView",
]