from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from hotels.models import Hotel

class StatsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        data = {
            "hotelsCount": Hotel.objects.count(),
            "formsCount": 100,        # mock
            "messagesCount": 30,      # mock
            "usersCount": 200,        # mock
            "emailsCount": 35,        # mock
            "entitiesCount": 4,       # mock
        }

        return Response({
            "success": True,
            "message": "Statistiques dashboard",
            "data": data
        }, status=200)
