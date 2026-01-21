
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
    photo_url = serializers.SerializerMethodField()

    class Meta:
        model = Hotel
        fields = "__all__"
        # ou si tu veux être explicite :
        # fields = ["id","nom","adresse","email","telephone","prix_par_nuit","devise","photo","photo_url","created_at","updated_at"]

    def get_photo_url(self, obj):
        request = self.context.get("request")
        if obj.photo and hasattr(obj.photo, "url"):
            return request.build_absolute_uri(obj.photo.url) if request else obj.photo.url
        return None
