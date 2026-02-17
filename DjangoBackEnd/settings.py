
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

# ✅ Mieux que ["*"] en prod (tu peux ajouter d'autres domaines si besoin)
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "").split(",") if not DEBUG else ["*"]
if not DEBUG and not ALLOWED_HOSTS:
    ALLOWED_HOSTS = [
        "red-product-backend-eymz.onrender.com",
        "localhost",
        "127.0.0.1",
    ]

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
# ⚠️ Recommandation: mets ces clés en env vars sur Render (ne pas hardcoder)
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
DOMAIN = os.environ.get("DOMAIN", "red-product-frontend-ten.vercel.app")
SITE_NAME = os.environ.get("SITE_NAME", "RED PRODUCT")
PROTOCOL = os.environ.get("PROTOCOL", ("https" if not DEBUG else "http"))

# =========================
# DJOSER
# =========================
DJOSER = {
    "LOGIN_FIELD": "email",
    "USER_CREATE_PASSWORD_RETYPE": False,

    "SEND_ACTIVATION_EMAIL": True,
    "SEND_CONFIRMATION_EMAIL": False,

    "USERNAME_CHANGED_EMAIL_CONFIRMATION": False,
    "PASSWORD_CHANGED_EMAIL_CONFIRMATION": False,

    "SET_USERNAME_RETYPE": False,
    "SET_PASSWORD_RETYPE": False,

    "ACTIVATION_URL": "activate/{uid}/{token}",
    "PASSWORD_RESET_CONFIRM_URL": "password-reset/{uid}/{token}",

    "DOMAIN": DOMAIN,
    "SITE_NAME": SITE_NAME,
    "PROTOCOL": PROTOCOL,

    "SERIALIZERS": {
        "user_create": "accounts.serializers.UserCreateSerializer",
        "user": "accounts.serializers.UserSerializer",
        "current_user": "accounts.serializers.UserSerializer",
    },
}

# =========================
# EMAIL CONFIG
# =========================
EMAIL_FAIL_SILENTLY = False

if DEBUG:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
else:
    # PROD (Render) : Brevo API (HTTPS)
    EMAIL_BACKEND = "accounts.email_backends.BrevoAPIEmailBackend"
    DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", "RED-PRODUCT <collefall118@gmial.com>")

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
# SECURITY
# =========================
DEBUG = os.environ.get("DEBUG", "True") == "True"

if DEBUG:
    ALLOWED_HOSTS = ["*"]
else:
    #  domaines autorisés en prod
    ALLOWED_HOSTS = [
        "red-product-backend-eymz.onrender.com",
        ".onrender.com",
        "localhost",
        "127.0.0.1",
    ]


# =========================
# LOGGING ( VOIR ERREURS SUR RENDER)
# =========================
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {"class": "logging.StreamHandler"},
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
    "loggers": {
        "django": {"handlers": ["console"], "level": "INFO", "propagate": False},
        "django.request": {"handlers": ["console"], "level": "ERROR", "propagate": False},
        "djoser": {"handlers": ["console"], "level": "DEBUG", "propagate": False},
        "accounts": {"handlers": ["console"], "level": "DEBUG", "propagate": False},
    },
}

# =========================
# DEFAULT PK
# =========================
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
