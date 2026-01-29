from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone
import uuid
from datetime import timedelta

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("L'adresse email est obligatoire")
        email = self.normalize_email(email)
        
        # Génération automatique du username
        if not extra_fields.get("username"):
            extra_fields["username"] = email.split("@")[0]
            
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    # Changement ici : null=True et plus de default fixe pour éviter les conflits
    username = models.CharField(max_length=150, unique=True, blank=True, null=True)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255, blank=True)
    
    # ⚠️ ON DÉSACTIVE EXPLICITEMENT LES CHAMPS QUI CAUSENT L'ERREUR 500
    first_name = None
    last_name = None
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

# Le reste de ton code (PasswordResetToken) est parfait, ne change rien.
class PasswordResetToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reset_tokens")
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def __str__(self):
        return f"Reset token for {self.user.email}"

    @classmethod
    def create_for(cls, user, hours=1):
        expires_at = timezone.now() + timedelta(hours=hours)
        return cls.objects.create(user=user, expires_at=expires_at)

    def is_valid(self):
        return timezone.now() < self.expires_at

    class Meta:
        ordering = ["-created_at"]