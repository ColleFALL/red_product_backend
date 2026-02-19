from django.urls import path
from .views import ChatbotView, ChatHistoryView, ClearConversationView

urlpatterns = [
    path('chat/', ChatbotView.as_view(), name='chatbot'),
    path('history/', ChatHistoryView.as_view(), name='chatbot-history'),
    path('clear/', ClearConversationView.as_view(), name='chatbot-clear'),
]