"""
Django settings for DjangoBackEnd project.
"""

from datetime import timedelta
import os
from pathlib import Path
import dj_database_url
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# =========================
# SECURITY
# =========================
SECRET_KEY = os.environ.get(
    "SECRET_KEY",
    "django-insecure-jbe62ob*y3$=ty3@w9(p7asx_22oe^9eo5o(z06&o#olbn!e3^"
)

DEBUG = os.environ.get("DEBUG", "True") == "True"
ALLOWED_HOSTS = ["*"]

# =========================
# APPS
# =========================
INSTALLED_APPS = [
    "cloudinary",
    "cloudinary_storage",

    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Tes apps
    "accounts",
    "hotels",
    "dashboard",

    # Tiers
    "rest_framework",
    "rest_framework_simplejwt",
    "django_filters",
    "rest_framework_simplejwt.token_blacklist",
    "djoser",
    "corsheaders",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "DjangoBackEnd.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "DjangoBackEnd.wsgi.application"

# =========================
# DATABASE
# =========================
DATABASES = {
    "default": dj_database_url.config(
        default=os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR / 'db.sqlite3'}"),
        conn_max_age=600,
    )
}

# =========================
# AUTH / PASSWORDS
# =========================
AUTH_USER_MODEL = "accounts.User"

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# =========================
# I18N
# =========================
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# =========================
# STATIC / MEDIA
# =========================
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# =========================
# CLOUDINARY
# =========================
import cloudinary
import cloudinary.uploader
import cloudinary.api

CLOUDINARY_STORAGE = {
    "CLOUD_NAME": os.environ.get("CLOUDINARY_CLOUD_NAME", "dxkadqzzz"),
    "API_KEY": os.environ.get("CLOUDINARY_API_KEY", "731133196691316"),
    "API_SECRET": os.environ.get("CLOUDINARY_API_SECRET", "dMXw_Vg15CsscxLbW5n1s5xA16Q"),
}

cloudinary.config(
    cloud_name=CLOUDINARY_STORAGE["CLOUD_NAME"],
    api_key=CLOUDINARY_STORAGE["API_KEY"],
    api_secret=CLOUDINARY_STORAGE["API_SECRET"],
    secure=True,
)

DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"

# =========================
# REST FRAMEWORK
# =========================
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 8,
}

# =========================
# JWT
# =========================
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=6),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": False,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
}

# =========================
# SITE / EMAIL LINKS (Djoser)
# =========================
# Domaine du frontend (là où l'utilisateur va cliquer)
DOMAIN = os.environ.get("DOMAIN", "red-product-frontend-ten.vercel.app")
SITE_NAME = os.environ.get("SITE_NAME", "RED PRODUCT")
PROTOCOL = "https" if not DEBUG else "http"

# =========================
# DJOSER (✅ ACTIVATION EMAIL)
# =========================
DJOSER = {
    "LOGIN_FIELD": "email",
    "USER_CREATE_PASSWORD_RETYPE": False,

    # ✅ IMPORTANT : activer l'email d'activation
    "SEND_ACTIVATION_EMAIL": True,
    # optionnel: email "compte créé"
    "SEND_CONFIRMATION_EMAIL": False,

    "USERNAME_CHANGED_EMAIL_CONFIRMATION": False,
    "PASSWORD_CHANGED_EMAIL_CONFIRMATION": False,

    "SET_USERNAME_RETYPE": False,
    "SET_PASSWORD_RETYPE": False,

    # ✅ Liens pour ton frontend
    "ACTIVATION_URL": "activate/{uid}/{token}",
    "PASSWORD_RESET_CONFIRM_URL": "password-reset/{uid}/{token}",

    # ✅ Indispensable pour construire les liens dans l'email
    "DOMAIN": DOMAIN,
    "SITE_NAME": SITE_NAME,
    "PROTOCOL": PROTOCOL,

    "SERIALIZERS": {
        "user_create": "accounts.serializers.UserCreateSerializer",
        "user": "accounts.serializers.UserSerializer",
        "current_user": "accounts.serializers.UserSerializer",
    },
}

# # =========================
# # EMAIL CONFIG
# # =========================
# if DEBUG:
#     # ✅ Dev: par défaut on affiche dans le terminal (pas d’envoi réel)
#     EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
# else:
#     # ✅ Prod: SMTP obligatoire
#     EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
#     EMAIL_HOST = os.environ.get("EMAIL_HOST", "smtp.gmail.com")
#     EMAIL_PORT = int(os.environ.get("EMAIL_PORT", "587"))
#     EMAIL_USE_TLS = os.environ.get("EMAIL_USE_TLS", "True") == "True"
#     EMAIL_USE_SSL = os.environ.get("EMAIL_USE_SSL", "False") == "True"
#     EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
#     EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
#     DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", EMAIL_HOST_USER)
#     EMAIL_TIMEOUT = int(os.environ.get("EMAIL_TIMEOUT", "30"))

#     if not EMAIL_HOST_USER or not EMAIL_HOST_PASSWORD:
#         raise ValueError("EMAIL_HOST_USER / EMAIL_HOST_PASSWORD manquants en prod")
# =========================
# EMAIL CONFIG
# =========================
if DEBUG:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
else:
    EMAIL_BACKEND = "accounts.email_backends.BrevoAPIEmailBackend"
    DEFAULT_FROM_EMAIL = os.environ.get(
        "DEFAULT_FROM_EMAIL",
        "RED PRODUCT <collefall118@gmail.com>"
    )



# =========================
# CORS / CSRF
# =========================
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:5173",
    "http://localhost:3000",
    "https://red-product-frontend-ten.vercel.app",
    "https://red-product-backend-eymz.onrender.com",
]
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://localhost:3000",
    "https://red-product-frontend-ten.vercel.app",
]
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOW_CREDENTIALS = False

CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]

CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]

# =========================
# SECURITY (PROD)
# =========================
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = "DENY"

# =========================
# DEFAULT PK
# =========================
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
