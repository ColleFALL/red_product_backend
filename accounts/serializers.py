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
        
        # ⚠️ Création de l'utilisateur ACTIF par défaut
        user = User.objects.create_user(**validated_data)
        
        # Attribution du name
        if name:
            user.name = name
            user.save()
        
        return user


class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        model = User
        fields = ('id', 'email', 'name', 'username', 'is_active', 'date_joined')
        read_only_fields = ('id', 'username', 'is_active', 'date_joined')