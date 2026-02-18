from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.conf import settings
from django.conf.urls.static import static


def home(request):
    return JsonResponse({"success": True, "message": "RED PRODUCT API is running"})


urlpatterns = [
    path("", home),
    path("admin/", admin.site.urls),
    
    # Djoser endpoints pour l'authentification
    path('api/auth/', include('djoser.urls')),
    path('api/auth/', include('djoser.urls.jwt')),
    
    # Vos apps
    path("api/", include("dashboard.urls")),
    path("api/hotels/", include("hotels.urls")),
    path('api/', include('chatbot.urls')),

]

# Servir les médias en dev
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)