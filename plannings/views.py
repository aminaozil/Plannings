from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator
from django.utils import timezone
from utilisateur import formulaire
from utilisateur.models import Matiere,Formateur, Apprenant
from .models import  Salle, Classe, Planning

@login_required
@permission_required('salle.view_salle', raise_exception=True)
def liste_salle(request):
    if request.method == "POST":
        nom_salle = request.POST["nom_salle"]
        Salle.objects.create(
            nom_salle = nom_salle,
        )
        return redirect("/liste_salle/")
    
    salles = Salle.objects.filter(archive=False)
    paginator = Paginator(salles, 5)
    nbre_page = request.GET.get('page')
    salles = paginator.get_page(nbre_page)
    return render(request, "planning/liste_salle.html", {"salles":salles}) 
  
@login_required
@permission_required('salle.change_apprenant', raise_exception=True)
def modifier_salle(request, id):
    salle = get_object_or_404(Salle, id=id)
    if request.method == "POST":
        nom_salle = request.POST["nom_salle"]
        salles = Salle.objects.filter(pk=id)
        salles.update(
            nom_salle=nom_salle,
        )
        return redirect("/liste_salle/")

    return render(request, "planning/modifier_salle.html", {"salle":salle}) 

@login_required
@permission_required('salle.delete_salle', raise_exception=True)
def supprimer_salle(request, id):
    salle = get_object_or_404(Salle, id=id)
    
    salle = Salle.objects.filter(pk=id)
    salle.update(
        archive=True
    )
    return redirect("/liste_salle/")


@login_required
def liste_classe(request):
    utilisateur = request.user
    formateur = Formateur.objects.get(user_formateur_id=utilisateur)
    planning = Planning.objects.filter(formateur=formateur)

    mes_classes = set(emploi.classe for emploi in planning)
    
    return render(request, "utilisateur/liste_classe.html", {"mes_classes":mes_classes})


@permission_required('planning.add_planning', raise_exception=True)
def create_planning(request):
    salles = Salle.objects.all()
    classes = Classe.objects.all()
    formateurs = None
    matieres = None
    selected_classe = None

    if request.method == 'POST':
        # Récupérer l'ID de la classe sélectionnée depuis le formulaire
        classe_id = request.POST.get('classe')
        selected_classe = Classe.objects.get(id=classe_id)

        # Récupérer les formateurs et matières associés à la classe via la filière
        filiere = selected_classe.filiere
        formateurs = Formateur.objects.filter(filiere=filiere)
        matieres = Matiere.objects.filter(matiere=filiere)
        # Si on veut créer un emploi du temps (submit pour emploi du temps)
        if 'create_emploi' in request.POST:
            date_debut = request.POST['date_debut']
            date_fin = request.POST['date_fin']
            date_debut = request.POST['date_debut']
            jour = request.POST['jour']
            heure_cours = request.POST['heure_cours']
            duree = request.POST['duree']
            classe_id = request.POST.get('classe')
            formateur_id = request.POST.get('formateur')
            salle_id = request.POST.get('salle_id')
            matiere_id = request.POST.get('matiere')

            try:
                date_debut = timezone.datetime.strptime(date_debut, '%Y-%m-%d')
                date_fin = timezone.datetime.strptime(date_fin, '%Y-%m-%d')
                heure_cours = timezone.datetime.strptime(heure_cours, '%H:%M')

            except ValueError:
                message = "Le format choisi est incorrect"
                return render(request, "planning/response.html", {"message":message})
            
            occupation_salle = Planning.objects.filter(salle_id=salle_id, date_debut=date_debut, date_fin=date_fin, jour=jour, heure_cours=heure_cours).exists()
            occupation_formateur = Planning.objects.filter(formateur_id=formateur_id, date_debut=date_debut, date_fin=date_fin, jour=jour, heure_cours=heure_cours).exists()
            occupation_classe = Planning.objects.filter(classe_id=classe_id, date_debut=date_debut, date_fin=date_fin, heure_cours=heure_cours, jour=jour)
            #on vérifie si la salle, le formateur ou classe est occupé avant de créer
            if occupation_salle:
                message = "La salle est occupée à cette date et heure"
                return render(request, "planning/response.html", {"message":message})
            elif occupation_formateur:
                message = "Le formateur choisi a cours à cette date et heure"
                return render(request, "planning/response.html", {"message":message})
            elif occupation_classe:
                message = "Le classe choisi a cours à cette date et heure"
                return render(request, "planning/response.html", {"message":message})

            else:
                # Récupérer les formateurs et matières associés à la filière de la classe sélectionnée
                salle = Salle.objects.get(id=salle_id)
                classe = Classe.objects.get(id=classe_id)
                formateur = Formateur.objects.get(id=formateur_id)
                matiere = Matiere.objects.get(id=matiere_id)

                Planning.objects.create(
                    date_debut=date_debut,
                    date_fin=date_fin,
                    jour=jour,
                    heure_cours=heure_cours,
                    duree=duree,
                    classe=classe,
                    formateur=formateur,
                    salle=salle,
                    matiere=matiere,
                )
                return redirect('/all_planning/')

    return render(request, 'planning/create_planning.html', {"formateurs":formateurs, "matieres":matieres, "salles":salles, "classes":classes, "selected_classe":selected_classe})


@login_required
def planning_formateur(request):
    utilisateur = request.user
    formateur = Formateur.objects.get(user_formateur_id=utilisateur)
    plannings = Planning.objects.filter(formateur=formateur)

    #Formulaire pour filter les dates pour l'affichage de l'emplois du temps
    form = formulaire.DateEdtFormateurForm(request.GET)

    if form.is_valid():
        date_debut = form.cleaned_data.get("date_debut")
        date_fin = form.cleaned_data.get("date_fin")
        classe = form.cleaned_data.get("classe")
        plannings = plannings.filter(date_debut__lte=date_debut, date_fin__gte=date_fin, classe__gte=classe)
        
    return render(request, "utilisateur/planning_formateur.html", {"plannings":plannings, "form":form})


def all_plannings(request):
    plannings = None
    #Formulaire pour filter les dates et classe pour l'affichage de l'emplois du temps
    form = formulaire.DateEdtFormateurForm(request.GET)

    if form.is_valid():
        date_debut = form.cleaned_data.get("date_debut")
        date_fin = form.cleaned_data.get("date_fin")
        classe = form.cleaned_data.get("classe")
        plannings = Planning.objects.filter(classe=classe).filter(date_debut__lte=date_debut, date_fin__gte=date_fin, classe__gte=classe)

    return render(request, "planning/plannings.html", {"plannings":plannings, "form":form})


@login_required
def planning_app(request):
    utilisateur = request.user
    apprenant = Apprenant.objects.get(user_apprenant_id=utilisateur)    
    classe = Classe.objects.get(apprenant=apprenant)
    planning = Planning.objects.filter(classe=classe)
    #Formulaire pour filter les dates pour l'affichage de l'emplois du temps
    form = formulaire.DateEdtForm(request.GET)

    if form.is_valid():
        date_debut = form.cleaned_data.get("date_debut")
        date_fin = form.cleaned_data.get("date_fin")
        planning = planning.filter(date_debut__lte=date_debut, date_fin__gte=date_fin)

    return render(request, "planning/planning_app.html", {"planning":planning, "form":form})
