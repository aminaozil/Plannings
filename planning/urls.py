from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.urls import include, path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("utilisateur.urls")),
    path('', include("plannings.urls")),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)