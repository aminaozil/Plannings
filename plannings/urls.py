from django.urls import path
from .views import modifier_salle,supprimer_salle, liste_salle,liste_classe, create_planning, planning_app, all_plannings, planning_formateur


urlpatterns = [
    #salle 
    path('liste_salle/',liste_salle , name="liste_salle"),
    path('modifier_salle/<int:id>/',modifier_salle , name="modifier_salle"),
    path('supprimer_salle/<int:id>/',supprimer_salle , name="supprimer_salle"),

    #classe
    path('liste_classe/',liste_classe , name="liste_classe"),

    #plannings

    path('create_planning/', create_planning, name="create_planning"),
    path('planning_apprenant/',planning_app, name="planning_apprenant"),
    path('all_planning/',all_plannings, name="all_planning"),
    path('planning_formateur/',planning_formateur , name="planning_formateur"),


    
]

