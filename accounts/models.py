from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('L\'adresse email est obligatoire')
        
        email = self.normalize_email(email)
        
        # ⚠️ Générer automatiquement le username depuis l'email
        if 'username' not in extra_fields:
            extra_fields['username'] = email.split('@')[0]
        
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Le superuser doit avoir is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Le superuser doit avoir is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True, blank=True, null=True) # Ajoute null=True
      # ⚠️ AJOUTÉ
    email = models.EmailField(unique=True, verbose_name='Email')
    name = models.CharField(max_length=255, blank=True, verbose_name='Nom complet')
    
    is_active = models.BooleanField(default=True)  # ⚠️ CHANGÉ: True par défaut
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # ⚠️ username requis pour createsuperuser

    class Meta:
        verbose_name = 'Utilisateur'
        verbose_name_plural = 'Utilisateurs'

    def __str__(self):
        return self.email