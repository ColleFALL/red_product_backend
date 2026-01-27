from rest_framework import serializers
from django.contrib.auth import get_user_model

from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        model = User
        fields = ('id', 'email', 'name', 'password')
    
    def create(self, validated_data):
        # Extraction du name
        name = validated_data.pop('name', '')
        
        # Génération automatique du username à partir de l'email
        email = validated_data.get('email')
        validated_data['username'] = email.split('@')[0]
        
        # Création de l'utilisateur (INACTIF par défaut)
        user = User.objects.create_user(**validated_data)
        
        # Attribution du name
        if name:
            user.name = name
            user.save()
        
        return user

class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        model = User
        fields = ('id', 'email', 'name', 'username', 'is_active')

# Admin = get_user_model()

# class RegisterSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True, min_length=6)
#     accept = serializers.BooleanField(write_only=True)

#     class Meta:
#         model = Admin
#         fields = ["name", "email", "password", "accept"]

#     def validate(self, attrs):
#         if attrs.get("accept") is not True:
#             raise serializers.ValidationError({"accept": "Vous devez accepter les termes."})
#         return attrs

#     def create(self, validated_data):
#         validated_data.pop("accept", None)
#         password = validated_data.pop("password")
#         user = Admin.objects.create_user(password=password, **validated_data)
#         return user

# class AdminPublicSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Admin
#         fields = ["id", "name", "email", "created_at"]
