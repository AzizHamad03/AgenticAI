from django.urls import path

from core.views import (
    CandidateCreateAPIView,
    InterviewQuestionSetDetailAPIView,
    JobPositionCreateAPIView,
    ResumeUploadAPIView,
    ScreeningResultDetailAPIView,
    TwilioWhatsAppWebhookView,
)


urlpatterns = [
    path(
        "job-positions/",
        JobPositionCreateAPIView.as_view(),
        name="job-position-create",
    ),
    path(
        "candidates/",
        CandidateCreateAPIView.as_view(),
        name="candidate-create",
    ),
    path(
        "resumes/",
        ResumeUploadAPIView.as_view(),
        name="resume-upload",
    ),
    path(
        "screening-results/<int:pk>/",
        ScreeningResultDetailAPIView.as_view(),
        name="screening-result-detail",
    ),
    path(
        "interview-question-sets/<int:pk>/",
        InterviewQuestionSetDetailAPIView.as_view(),
        name="interview-question-set-detail",
    ),
    path(
        "whatsapp/webhook/",
        TwilioWhatsAppWebhookView.as_view(),
        name="whatsapp-webhook",
    ),
]