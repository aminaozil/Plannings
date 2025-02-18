from .views import login_view, logout_view, accueil, create_formateur, modifier_formateur,list_filiere, tableau_admin, send_emails,supprimer_matiere, modifier_matiere, liste_matiere, info_planning,supprimer_formateur, liste_formateur, liste_apprenant, create_apprenant, modifier_apprenant, info_utilisateur
from django.urls import path


urlpatterns = [
    path("", accueil, name="accueil"),


    # authentification

    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path('info_utilisateur/',info_utilisateur , name="info_utilisateur"),
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
