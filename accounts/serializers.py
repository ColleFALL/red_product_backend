from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        model = User
        fields = ('id', 'email', 'name', 'password')
        # ⚠️ AJOUT : Exclure username des champs requis
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def create(self, validated_data):
        # Extraction du name
        name = validated_data.pop('name', '')
        
        # ⚠️ Génération automatique du username AVANT la création
        email = validated_data.get('email')
        username = email.split('@')[0]
        
        # ⚠️ Vérifier si le username existe déjà et le rendre unique
        base_username = username
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1
        
        # ⚠️ Ajouter le username aux données validées
        validated_data['username'] = username
        
        # Création de l'utilisateur
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