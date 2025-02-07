from .views import list_user, login_view, logout_view, accueil, create_formateur, modifier_formateur,supprimer_formateur, liste_formateur, liste_apprenant, create_apprenant, modifier_apprenant, create_planning
from django.urls import path


urlpatterns = [
    path("", accueil, name="accueil"),
    path("list_user/", list_user, name="list_user"),

    # authentification

    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    
    #formateur

    path('create_formateur/',create_formateur, name="create_formateur"),
    path('liste_formateur/',liste_formateur, name="liste_formateur"),
    path('modifier_formateur/<int:id>', modifier_formateur, name="modifier_formateur"),
    path('supprimer_formateur/<int:id>', supprimer_formateur, name="supprimer_formateur"),

    #apprenant

    path('liste_apprenant/', liste_apprenant, name="liste_apprenant"),
    path('create_apprenant/', create_apprenant, name="create_apprenant"),
    path('modifier_apprenant/<int:id>', modifier_apprenant, name="modifier_apprenant"),

    #plannings

    path('create_planning/', create_planning, name="create_planning"),
    
]
