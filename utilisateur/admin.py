from django.contrib import admin
from .models import User, Matiere, Filiere, Formateur, Apprenant

admin.site.register(User)
admin.site.register(Filiere)
admin.site.register(Formateur) 
admin.site.register(Matiere)
admin.site.register(Apprenant)
