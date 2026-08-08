from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import ScreeningResult
from core.serializers import ScreeningResultSerializer


class ScreeningResultDetailAPIView(APIView):

    def get(self, request, pk):
        try:
            screening_result = ScreeningResult.objects.get(pk=pk)

            serializer = ScreeningResultSerializer(screening_result)

            return Response(
                serializer.data,
                status=status.HTTP_200_OK,
            )

        except ScreeningResult.DoesNotExist:
            return Response(
                {"detail": "Screening result not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        except Exception as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )