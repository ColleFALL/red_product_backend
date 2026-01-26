from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Hotel
from .serializers import HotelSerializer
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.permissions import AllowAny

class HotelViewSet(viewsets.ModelViewSet):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
    permission_classes = [AllowAny]

    # ✅ Pour gérer les uploads de fichiers via FormData
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    # ✅ Recherche + tri
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["nom", "adresse"]
    ordering_fields = ["created_at", "prix_par_nuit", "nom"]

    def perform_create(self, serializer):
        """
        Surcharge pour accepter le fichier local uploadé
        """
        serializer.save()

    def perform_update(self, serializer):
        """
        Même chose pour la mise à jour
        """
        serializer.save()
