from rest_framework import serializers
from .models import Hotel

class HotelSerializer(serializers.ModelSerializer):
    photo_url = serializers.SerializerMethodField()

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
            "photo",
            "photo_url",
            "created_at",
            "updated_at",
        ]

    def get_photo_url(self, obj):
        request = self.context.get("request")
        if obj.photo and hasattr(obj.photo, "url"):
            return request.build_absolute_uri(obj.photo.url) if request else obj.photo.url
        return None

    def validate(self, attrs):
    if self.instance is None:  # création
        required = ["nom", "adresse", "prix_par_nuit", "devise", "photo"]
        missing = [f for f in required if not attrs.get(f)]
        if missing:
            raise serializers.ValidationError({f: "Champ obligatoire" for f in missing})
    return attrs

