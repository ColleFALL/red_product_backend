from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        model = User
        fields = ('id', 'email', 'name', 'password')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        # On passe tout au UserManager (email, password, name)
        # Il s'occupera du username tout seul
        return User.objects.create_user(**validated_data)

class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        model = User
        fields = ('id', 'email', 'name', 'username', 'is_active', 'date_joined')
        read_only_fields = ('id', 'username', 'is_active', 'date_joined')