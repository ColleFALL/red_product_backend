from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Hotel
from .serializers import HotelSerializer

class HotelViewSet(viewsets.ModelViewSet):
    queryset = Hotel.objects.all().order_by("-created_at")
    serializer_class = HotelSerializer
    permission_classes = [permissions.IsAuthenticated]

    # BE-9 : Recherche + tri (pagination DRF déjà active via settings)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["nom", "adresse"]
    ordering_fields = ["created_at", "prix_par_nuit", "nom"]
