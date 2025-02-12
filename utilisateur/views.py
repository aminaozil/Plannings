from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from . import forms
from .models import Formateur, Filiere, User, Apprenant, Classe, Matiere,Planning, Salle
from django.contrib import messages
from django.core.paginator import Paginator
from django.utils import timezone

# Create your views here.

def list_user(request):
    return render(request, "utilisateur/list_user.html")

def accueil(request):
    return render(request, "utilisateur/accueil.html")



""" authentification """

def login_view(request):
    form = forms.LoginForm()
    message = ''
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                return redirect("/info_utilisateur/")
            else:
                messages.error(request, "Email ou mot de passe incorrect")
    return render(request, "utilisateur/login.html", context={'form': form, 'message': message})

def logout_view(request):
    
    logout(request)
    return redirect('login')

""" Formateur """

def create_formateur(request):
    form = forms.FormateurForm()
    if request.method == "POST":
        user_formateur = request.POST.get('user_formateur')
        nom = request.POST['nom']
        prenom = request.POST['prenom']
        specialite = request.POST['specialite']
        email = request.POST['email']
        filiere = request.POST['filiere']

        formateurs = Formateur.objects.create(
            user_formateur = User.objects.get(id=user_formateur) ,
            nom = nom,
            prenom = prenom,
            specialite = specialite,
            email = email,
            

        )
        formateurs.save()
        formateurs.filiere.add(filiere)
        

        return redirect("/liste_formateur/")
    
    return render(request, "utilisateur/create_formateur.html", {"form":form})

def modifier_formateur(request, id):
    formateur = Formateur.objects.get(id=id)
    form = forms.FormateurForm(request.POST or None, instance=formateur)
    if form.is_valid():
        form.save()
        return redirect("/liste_formateur/")
    return render(request, "utilisateur/modifier_formateur.html", {"formateur": formateur, "form":form})

def supprimer_formateur(request, id=id):
    formateur = Formateur.objects.get(id=id)
    if request.method == "POST":
        sup_formateurs = Formateur.objects.filter(pk=formateur.id)
        sup_formateurs.update(
            archive=True
        )
        redirect("/liste_formateur/")

    return render(request, "utilisateur/supprimer_formateur.html", {"formateur":formateur})

def liste_formateur(request):
    formateurs = Formateur.objects.filter(archive=False)
    paginator = Paginator(formateurs, 4)
    page_number = request.GET.get('page')
    prof = paginator.get_page(page_number)
    if request.method == "GET":
        name = request.GET.get("recherche")
        if name is not None:
            prof = Formateur.objects.filter(prenom__icontains=name)

    return render(request, "utilisateur/liste_formateur.html", {"prof":prof})


""" apprenant """

def liste_apprenant(request):
    etudiant = Apprenant.objects.filter(archive=False)
    paginator = Paginator(etudiant, 4)
    page_number = request.GET.get('page')
    apprenants = paginator.get_page(page_number)
    if request.method == "GET":
        name = request.GET.get("recherche")
        if name is not None:
            apprenants = Apprenant.objects.filter(prenom__icontains=name)

    

    return render(request, "utilisateur/liste_apprenant.html", {"apprenants": apprenants})

def create_apprenant(request):
    form = forms.ApprenantForm()
    if request.method == "POST":
        user_apprenant = request.POST.get('user_apprenant')
        nom = request.POST['nom']
        prenom = request.POST['prenom']
        email = request.POST['email']
        classe_apprenant = request.POST['classe_apprenant']
        
        

        apprenants = Apprenant.objects.create(
            user_apprenant = User.objects.get(id=user_apprenant) ,
            nom = nom,
            prenom = prenom,
            email = email,
            classe_apprenant = Classe.objects.get(id=classe_apprenant),
            

        )
        apprenants.save()

        return redirect("/liste_apprenant/")

    return render(request, "utilisateur/create_apprenant.html", {"form":form})

def modifier_apprenant(request, id):
    apprenant = Apprenant.objects.get(id=id)
    form = forms.ApprenantForm(request.POST or None, instance=apprenant)
    if form.is_valid():
        form.save()
        return redirect("/liste_apprenant/")
    return render(request, "utilisateur/modifier_apprenant.html", {"apprenant": apprenant, "form":form})


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
                return redirect('/liste_formateur/')

    return render(request, 'planning/create_planning.html', {"formateurs":formateurs, "matieres":matieres, "salles":salles, "classes":classes, "selected_classe":selected_classe})

def info_utilisateur(request):
    utilisateur = request.user
    #on vérifie si l'utilisateur connecté est un formateur ou apprenant
    try:
        
        info_form = Formateur.objects.get(user_formateur_id=utilisateur)
        

    # Récupérer les emplois du temps du formateur
        planning = Planning.objects.filter(formateur=info_form)

    # Extraire les classes associées auformateur connecté à travers son emploi du temps
        mes_classes = set(emploi.classe for emploi in planning)
        
        
       
        return render(request, "utilisateur/info_formateur.html", {"info_form":info_form, "mes_classes":mes_classes})

    except Formateur.DoesNotExist:
    #si l'utilisateur n'est un formateur, il vérifie si est appprenant
        try:
            info_app = Apprenant.objects.filter(user_apprenant_id=utilisateur)
            return render(request,"utilisateur/info_app.html", {"info_app":info_app})
        except Apprenant.DoesNotExist:
            sms="code marche pas"
            return render(request, "utilisateur/info_app.html", {"sms": sms})

def liste_classe(request):
    utilisateur = request.user
    formateur = Formateur.objects.get(user_formateur_id=utilisateur)
    planning = Planning.objects.filter(formateur=formateur)

    mes_classes = set(emploi.classe for emploi in planning)
    
    return render(request, "utilisateur/liste_classe.html", {"mes_classes":mes_classes})

def planning_formateur(request):
    utilisateur = request.user
    formateur = Formateur.objects.get(user_formateur_id=utilisateur)
    plannings = Planning.objects.filter(formateur=formateur)
    return render(request, "utilisateur/planning_formateur.html", {"plannings":plannings})

def info_planning(request, id):
    planning = get_object_or_404(Planning, id=id) 
    return render(request, "planning/info_planning.html", {"planning":planning})

def planning_app(request):
    utilisateur = request.user
    apprenant = Apprenant.objects.get(user_apprenant_id=utilisateur)    
    classe = Classe.objects.get(apprenant=apprenant)
    planning = Planning.objects.filter(classe=classe)
    #Formulaire pour filter les dates pour l'affichage de l'emplois du temps
    form = forms.DateEdtForm(request.GET)

    if form.is_valid():
        date_debut = form.cleaned_data.get("date_debut")
        date_fin = form.cleaned_data.get("date_fin")
        planning = planning.filter(date_debut__gte=date_debut, date_fin__lte=date_fin)

    return render(request, "planning/planning_app.html", {"planning":planning, "form":form})

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
  
def supprimer_salle(request, id):
    salle = get_object_or_404(Salle, id=id)
    
    salle = Salle.objects.filter(pk=id)
    salle.update(
        archive=True
    )
    return redirect("/liste_salle/") 

def liste_matiere(request):
    if request.method == "POST":
        nom_matiere = request.POST["nom_matiere"]
        Matiere.objects.create(
            nom_matiere = nom_matiere,
        )
        return redirect("/liste_matiere/")
    
    matieres = Matiere.objects.filter(archive=False)
    paginator = Paginator(matieres, 5)
    nbre_page = request.GET.get('page')
    matieres = paginator.get_page(nbre_page)
    return render(request, "planning/liste_matiere.html", {"matieres":matieres})   

def modifier_matiere(request, id):
    matiere = get_object_or_404(Matiere, id=id)
    if request.method == "POST":
        nom_matiere = request.POST["nom_matiere"]
        matieres = Matiere.objects.filter(pk=id)
        matieres.update(
            nom_matiere=nom_matiere,
        )
        return redirect("/liste_matiere/")

    return render(request, "planning/modifier_matiere.html", {"matiere":matiere}) 

def supprimer_matiere(request, id):
    matiere = get_object_or_404(Matiere, id=id)
    
    matiere = Matiere.objects.filter(pk=id)
    matiere.update(
        archive=True
    )
    return redirect("/liste_matiere/")
    