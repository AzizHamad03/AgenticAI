from pathlib import Path

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
        fields = [
            "id",
            "name",
            "description",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
        ]


class JobPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobPosition
        fields = [
            "id",
            "title",
            "department",
            "description",
            "created_at",
            "required_skills",
        ]
        read_only_fields = [
            "id",
            "created_at",
        ]

    def validate_required_skills(self, value):
        if not isinstance(value, list):
            raise serializers.ValidationError(
                "Required skills must be a list."
            )

        if not all(isinstance(skill, str) for skill in value):
            raise serializers.ValidationError(
                "Each required skill must be a string."
            )

        return value


class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = [
            "id",
            "full_name",
            "email",
            "phone",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
        ]


class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = [
            "id",
            "candidate",
            "file",
            "uploaded_at",
        ]
        read_only_fields = [
            "id",
            "uploaded_at",
        ]

    def validate_file(self, value):
        allowed_extensions = [".pdf", ".docx", ".txt"]

        extension = Path(value.name).suffix.lower()

        if extension not in allowed_extensions:
            raise serializers.ValidationError(
                "Only PDF, DOCX, and TXT files are allowed."
            )

        return value


class ScreeningResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScreeningResult
        fields = [
            "id",
            "candidate",
            "job_position",
            "score",
            "strengths",
            "missing_skills",
            "recommendation",
            "summary",
            "raw_report",
            "generated_at",
        ]
        read_only_fields = [
            "id",
            "generated_at",
        ]


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
        read_only_fields = [
            "id",
            "generated_at",
        ]


class RunActionSerializer(serializers.Serializer):
    candidate_id = serializers.IntegerField()
    job_position_id = serializers.IntegerField()