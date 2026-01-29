
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class UserCreateSerializer(BaseUserCreateSerializer):
    """Serializer pour la création d'utilisateur avec Djoser"""
    class Meta(BaseUserCreateSerializer.Meta):
        model = User
        fields = ("id", "email", "name", "password")
        extra_kwargs = {
            "password": {"write_only": True},
            "name": {"required": False}
        }

    def create(self, validated_data):
        # Le username sera généré automatiquement dans UserManager
        return User.objects.create_user(**validated_data)


class UserSerializer(BaseUserSerializer):
    """Serializer pour afficher les informations utilisateur"""
    class Meta(BaseUserSerializer.Meta):
        model = User
        fields = ("id", "email", "name", "username", "is_active", "date_joined")
        read_only_fields = ("id", "username", "is_active", "date_joined")