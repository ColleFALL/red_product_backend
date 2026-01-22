
# from rest_framework import serializers
# from .models import Hotel


# class HotelSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Hotel
#         fields = "__all__"

#     def validate(self, attrs):
#         """
#         Validation globale (optionnelle)
#         """
#         return attrs

#     def create(self, validated_data):
#         """
#         Création d'un hôtel
#         """
#         return Hotel.objects.create(**validated_data)

#     def update(self, instance, validated_data):
#         """
#         Mise à jour d'un hôtel
#         """
#         for attr, value in validated_data.items():
#             setattr(instance, attr, value)
#         instance.save()
#         return instance


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
            return obj.photo.url  # ✅ Cloudinary URL
        return None
