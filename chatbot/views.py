from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Conversation, Message
from .services.gemini_service import ask_gemini
from .services.context_service import build_context

class ChatbotView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        message = request.data.get("message")

        if not message:
            return Response(
                {"success": False, "message": "Message requis"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # 1️⃣ Récupérer ou créer conversation
            conversation, created = Conversation.objects.get_or_create(
                admin=request.user
            )

            # 2️⃣ Sauvegarder message user
            Message.objects.create(
                conversation=conversation,
                role="user",
                content=message
            )

            # 3️⃣ Construire contexte
            context_data = build_context()

            # 4️⃣ Récupérer historique
            history = list(
                conversation.messages
                .values("role", "content")
                .order_by("created_at")
            )

            # 5️⃣ Appel Gemini
            reply = ask_gemini(message, context_data, history)

            # 6️⃣ Sauvegarder réponse
            Message.objects.create(
                conversation=conversation,
                role="assistant",
                content=reply
            )

            return Response({
                "success": True,
                "data": {
                    "reply": reply
                }
            })

        except Exception as e:
            return Response(
                {"success": False, "message": "Erreur chatbot"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
class ChatHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            conversation = Conversation.objects.filter(admin=request.user).first()
            if not conversation:
                return Response({"success": True, "data": {"messages": []}})

            messages = list(
                conversation.messages
                .values("role", "content", "created_at")
                .order_by("created_at")
            )

            return Response({"success": True, "data": {"messages": messages}})

        except Exception as e:
            return Response(
                {"success": False, "message": "Erreur"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
class ClearConversationView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        try:
            Conversation.objects.filter(admin=request.user).delete()
            return Response({"success": True, "message": "Conversation supprimée"})
        except Exception as e:
            return Response(
                {"success": False, "message": "Erreur"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )