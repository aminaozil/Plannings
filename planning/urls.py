from django.contrib import admin
from django.urls import include, path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("utilisateur.urls")),
    path('', include("plannings.urls")),
]

urlpatterns += staticfiles_urlpatterns()
