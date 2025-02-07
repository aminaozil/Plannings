from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from . import forms
from .models import Formateur, Filiere, User, Apprenant, Classe, Matiere,Planning, Salle
from django.contrib import messages
from django.core.paginator import Paginator

# Create your views here.

def list_user(request):
    return render(request, "utilisateur/list_user.html")

def accueil(request):
    return render(request, "utilisateur/accueil.html")

def logout_view(request):
    
    logout(request)
    return redirect('login')

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
                return redirect("/liste_formateur/")
            else:
                messages.error(request, "Email ou mot de passe incorrect")
    return render(request, "utilisateur/login.html", context={'form': form, 'message': message})

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

        # Récupérer les professeurs et matières associés à la classe via la filière
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