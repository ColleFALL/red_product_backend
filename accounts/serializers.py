from rest_framework import serializers
from django.contrib.auth import get_user_model

Admin = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    accept = serializers.BooleanField(write_only=True)

    class Meta:
        model = Admin
        fields = ["name", "email", "password", "accept"]

    def validate(self, attrs):
        if attrs.get("accept") is not True:
            raise serializers.ValidationError({"accept": "Vous devez accepter les termes."})
        return attrs

    def create(self, validated_data):
        validated_data.pop("accept", None)
        password = validated_data.pop("password")
        user = Admin.objects.create_user(password=password, **validated_data)
        return user

class AdminPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = ["id", "name", "email", "created_at","photo"]
