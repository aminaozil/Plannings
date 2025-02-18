from django.contrib import admin
from .models import Salle, Classe, Planning

admin.site.register(Salle)
admin.site.register(Classe)
admin.site.register(Planning)