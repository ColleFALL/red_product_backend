

from rest_framework import serializers
from .models import Hotel

class HotelSerializer(serializers.ModelSerializer):
    photo_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Hotel
        fields = [
            "id",
            "nom",
            "adresse",
            "email",
            "telephone",
            "prix_par_nuit",
            "devise",
            "photo",        # upload
            "photo_url",    # affichage
            "created_at",
            "updated_at",
        ]

    def get_photo_url(self, obj):
        if obj.photo:
            return obj.photo  # ✅ Cloudinary URL
        return None
