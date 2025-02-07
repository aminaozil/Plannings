from django.contrib import admin
from .models import User, Formateur, Filiere, Matiere, Classe, Apprenant, Salle, Planning

admin.site.register(User)
admin.site.register(Filiere)
admin.site.register(Formateur)
admin.site.register(Matiere)
admin.site.register(Classe)
admin.site.register(Apprenant)
admin.site.register(Salle)
admin.site.register(Planning)