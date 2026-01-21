
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.conf import settings
from django.conf.urls.static import static

def home(request):
    return JsonResponse({"success": True, "message": "RED PRODUCT API is running"})

urlpatterns = [
    path("", home),  #  racine /
    path("admin/", admin.site.urls),
    # DRF login (optionnel)
     path("api/auth/", include("accounts.urls")),
     path("api/", include("dashboard.urls")),
     path("api/hotels/", include("hotels.urls")),

]
#  servir les médias en dev (photos)
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# servir les médias (MVP Render)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

