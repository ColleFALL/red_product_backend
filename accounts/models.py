from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

# mdp
import uuid
from datetime import timedelta
from django.utils import timezone



class AdminManager(BaseUserManager):
    def create_user(self, email, password=None, name="", **extra_fields):
        if not email:
            raise ValueError("Email obligatoire")
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(password)  #  hash automatique
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, name="Admin", **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        return self.create_user(email=email, password=password, name=name, **extra_fields)
        
class Admin(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=120)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    photo = models.ImageField(upload_to="admins/", null=True, blank=True)


    objects = AdminManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    def __str__(self):
        return self.email


#mdp
class PasswordResetToken(models.Model):
    admin = models.ForeignKey("Admin", on_delete=models.CASCADE, related_name="reset_tokens")
    token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def create_for(admin, hours=1):
        return PasswordResetToken.objects.create(
            admin=admin,
            expires_at=timezone.now() + timedelta(hours=hours),
        )

    def is_valid(self):
        return timezone.now() < self.expires_at