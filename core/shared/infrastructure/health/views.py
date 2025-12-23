from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .health_service import HealthService


class HealthCheckView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        result = HealthService().run()

        http_status = (
            status.HTTP_200_OK
            if result["status"] == "ok"
            else status.HTTP_503_SERVICE_UNAVAILABLE
        )

        return Response(result, status=http_status)
