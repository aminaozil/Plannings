from .views import login_view, logout_view, accueil, create_formateur, modifier_formateur,list_filiere, tableau_admin,all_plannings, send_emails,planning_app,supprimer_matiere, modifier_matiere, liste_matiere, modifier_salle,supprimer_salle, liste_salle, info_planning,liste_classe,planning_formateur, supprimer_formateur, liste_formateur, liste_apprenant, create_apprenant, modifier_apprenant, create_planning, info_utilisateur
from django.urls import path


urlpatterns = [
    path("", accueil, name="accueil"),


    # authentification

    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path('info_utilisateur/',info_utilisateur , name="info_utilisateur"),
    path('liste_classe/',liste_classe , name="liste_classe"),
    path('planning_formateur/',planning_formateur , name="planning_formateur"),
    path('info_planning/<int:id>/',info_planning , name="info_planning"),
    
    
    #formateur

    path('create_formateur/',create_formateur, name="create_formateur"),
    path('liste_formateur/',liste_formateur, name="liste_formateur"),
    path('modifier_formateur/<int:id>/', modifier_formateur, name="modifier_formateur"),
    path('supprimer_formateur/<int:id>/', supprimer_formateur, name="supprimer_formateur"),

    #apprenant

    path('liste_apprenant/', liste_apprenant, name="liste_apprenant"),
    path('create_apprenant/', create_apprenant, name="create_apprenant"),
    path('modifier_apprenant/<int:id>', modifier_apprenant, name="modifier_apprenant"),

    #plannings

    path('create_planning/', create_planning, name="create_planning"),
    path('planning_apprenant/',planning_app, name="planning_apprenant"),
    path('all_planning/',all_plannings, name="all_planning"),

    #salle 
    path('liste_salle/',liste_salle , name="liste_salle"),
    path('modifier_salle/<int:id>/',modifier_salle , name="modifier_salle"),
    path('supprimer_salle/<int:id>/',supprimer_salle , name="supprimer_salle"),

    #matiere
    path('liste_matiere/',liste_matiere , name="liste_matiere"),
    path('modifier_matiere/<int:id>/',modifier_matiere , name="modifier_matiere"),
    path('supprimer_matiere/<int:id>/',supprimer_matiere , name="supprimer_matiere"),

    #send email
    path('send_mail/',send_emails , name="send_mail"),

    #administration 
    path('tableau_administrateur/',tableau_admin , name="tableau_admin"),

    #filiere
    path('liste_filiere/',list_filiere , name="liste_filiere"),
]
