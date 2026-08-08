from rest_framework import serializers

from core.models import (
    Candidate,
    Department,
    InterviewQuestionSet,
    JobPosition,
    Resume,
    ScreeningResult,
)


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ["id", "name", "description", "created_at"]
        read_only_fields = ["id", "created_at"]

class JobPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobPosition
        fields = ["id", "title", "department", "description", "created_at", "required_skills"]
        read_only_fields = ["id", "created_at"]

class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = ["id", "full_name", "email", "phone_number", "created_at"]
        read_only_fields = ["id", "created_at"] 

class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = ["id", "candidate", "file", "uploaded_at"]
        read_only_fields = ["id", "uploaded_at"]    

class ScreeningResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScreeningResult
        fields = ["id", "candidate", "job_position", "score", "feedback", "created_at"]
        read_only_fields = ["id", "created_at"] 

class InterviewQuestionSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterviewQuestionSet
        fields = [
            "id",
            "candidate",
            "job_position",
            "screening_result",
            "technical_questions",
            "behavioral_questions",
            "follow_up_questions",
            "generated_at",
        ]
        read_only_fields = ["id", "generated_at"]

class RunActionSerializer(serializers.Serializer):
    candidate_id = serializers.IntegerField()
    job_position_id = serializers.IntegerField()

