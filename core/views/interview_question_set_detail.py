from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import InterviewQuestionSet
from core.serializers import InterviewQuestionSetSerializer


class InterviewQuestionSetDetailAPIView(APIView):

    def get(self, request, pk):
        try:
            question_set = InterviewQuestionSet.objects.get(pk=pk)

            serializer = InterviewQuestionSetSerializer(question_set)

            return Response(
                serializer.data,
                status=status.HTTP_200_OK,
            )

        except InterviewQuestionSet.DoesNotExist:
            return Response(
                {"detail": "Interview question set not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        except Exception as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )