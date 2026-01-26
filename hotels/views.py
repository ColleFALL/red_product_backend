from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Hotel
from .serializers import HotelSerializer
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.permissions import AllowAny

class HotelViewSet(viewsets.ModelViewSet):
    queryset = Hotel.objects.all()
    # queryset = Hotel.objects.all().order_by("-created_at")
    serializer_class = HotelSerializer
    permission_classes = [AllowAny]

    parser_classes = [ FormParser, JSONParser]  # ✅ AJOUT
    # BE-9 : Recherche + tri (pagination DRF déjà active via settings)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["nom", "adresse"]
    ordering_fields = ["created_at", "prix_par_nuit", "nom"]
