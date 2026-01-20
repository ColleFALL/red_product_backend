from django.contrib.auth import authenticate, get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework_simplejwt.tokens import RefreshToken
#mdp
from .models import PasswordResetToken
from .serializers import RegisterSerializer, AdminPublicSerializer
#resetmdp
from .models import PasswordResetToken
#photo
from rest_framework.parsers import MultiPartParser, FormParser


Admin = get_user_model()

def ok(message="", data=None, code=200):
    return Response({"success": True, "message": message, "data": data}, status=code)

def fail(message="", data=None, code=400):
    return Response({"success": False, "message": message, "data": data}, status=code)

class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return fail("Validation error", serializer.errors, 400)

        email = serializer.validated_data["email"].lower().strip()

        # 409 si email existe déjà
        if Admin.objects.filter(email=email).exists():
            return fail("Email déjà utilisé", None, 409)

        user = serializer.save(email=email)
        return ok("Compte créé", AdminPublicSerializer(user).data, 201)

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = (request.data.get("email") or "").lower().strip()
        password = request.data.get("password") or ""
        remember = bool(request.data.get("remember", False))

        if not email or not password:
            return fail("Email et mot de passe requis", None, 400)

        # ✅ Auth manuelle (robuste avec user custom)
        user = Admin.objects.filter(email=email).first()
        if not user or not user.check_password(password):
            return fail("Identifiants invalides", None, 401)

        if not user.is_active:
            return fail("Compte désactivé", None, 403)

        refresh = RefreshToken.for_user(user)
        access = str(refresh.access_token)

        data = {
            "access": access,
            "refresh": str(refresh),
            "admin": AdminPublicSerializer(user).data,
            "remember": remember,
        }
        return ok("Connecté", data, 200)

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = (request.data.get("email") or "").lower().strip()
        password = request.data.get("password") or ""
        remember = bool(request.data.get("remember", False))

        if not email or not password:
            return fail("Email et mot de passe requis", None, 400)

        user = authenticate(request, email=email, password=password)
        if not user:
            return fail("Identifiants invalides", None, 401)

        refresh = RefreshToken.for_user(user)
        access = str(refresh.access_token)

        data = {
            "access": access,
            "refresh": str(refresh),
            "admin": AdminPublicSerializer(user).data,
            "remember": remember,
        }
        return ok("Connecté", data, 200)

class MeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return ok("Profil", AdminPublicSerializer(request.user).data, 200)

#mdp
class ForgotPasswordView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = (request.data.get("email") or "").lower().strip()

        # ✅ réponse générique (sécurité)
        if not email:
            return ok("Si cet email existe, vous recevrez un message.", None, 200)

        user = Admin.objects.filter(email=email).first()
        if user:
            prt = PasswordResetToken.create_for(user, hours=1)

            # ✅ MOCK email : on log en console (plus tard SMTP)
            print(f"[FORGOT PASSWORD] email={email} token={prt.token} expires={prt.expires_at}")

        return ok("Si cet email existe, vous recevrez un message.", None, 200)
#reset mdp
class ResetPasswordView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        token = request.data.get("token")
        new_password = request.data.get("new_password") or ""

        if not token or not new_password:
            return fail("Token et nouveau mot de passe requis", None, 400)

        prt = PasswordResetToken.objects.filter(token=token).first()
        if not prt or not prt.is_valid():
            return fail("Token invalide ou expiré", None, 400)

        admin = prt.admin
        admin.set_password(new_password)  # ✅ hash Django
        admin.save()

        # ✅ on invalide le token après usage
        prt.delete()

        return ok("Mot de passe mis à jour", None, 200)
#photo
class AvatarView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        file = request.FILES.get("photo")  # ✅ le champ attendu côté front

        if not file:
            return fail("Photo requise", None, 400)

        user = request.user
        user.photo = file
        user.save()

        return ok("Photo mise à jour", AdminPublicSerializer(user).data, 200)
