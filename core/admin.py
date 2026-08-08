from django.contrib import admin

from core.models import (
    Candidate,
    Department,
    InterviewQuestionSet,
    JobPosition,
    Resume,
    ScreeningResult,
)


admin.site.register(Department)
admin.site.register(JobPosition)
admin.site.register(Candidate)
admin.site.register(Resume)
admin.site.register(ScreeningResult)
admin.site.register(InterviewQuestionSet)