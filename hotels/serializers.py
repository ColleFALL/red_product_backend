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
            # "photo_url",    # affichage
            "created_at",
            "updated_at",
        ]
    def get_photo_url(self, obj):
        request = self.context.get("request")
        if obj.photo:
            if request:
                return request.build_absolute_uri(obj.photo.url)  # lien complet pour le frontend
            return obj.photo.url  # juste le chemin relatif si pas de request
        return None
