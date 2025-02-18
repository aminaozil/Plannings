from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.core.mail import send_mail
from plannings.models import Classe, Planning
from . import formulaire
from .models import Formateur, User, Apprenant, Matiere, Filiere

def accueil(request):
    return render(request, "utilisateur/accueil.html")


""" authentification """


def login_view(request):
    form = formulaire.LoginForm()
    message = ''
    if request.method == 'POST':
        form = formulaire.LoginForm(request.POST)
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

@login_required
@permission_required('formateur.add_formateur', raise_exception=True)
def create_formateur(request):
    form = formulaire.FormateurForm()
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

@permission_required('formateur.change_formateur', raise_exception=True)
def modifier_formateur(request, id):
    formateur = Formateur.objects.get(id=id)
    form = formulaire.FormateurForm(request.POST or None, instance=formateur)
    if form.is_valid():
        form.save()
        return redirect("/liste_formateur/")
    return render(request, "utilisateur/modifier_formateur.html", {"formateur": formateur, "form":form})

@permission_required('formateur.delete_formateur', raise_exception=True)
def supprimer_formateur(request, id=id):
    formateur = Formateur.objects.get(id=id)
    if request.method == "POST":
        sup_formateurs = Formateur.objects.filter(pk=formateur.id)
        sup_formateurs.update(
            archive=True
        )
        redirect("/liste_formateur/")

    return render(request, "utilisateur/supprimer_formateur.html", {"formateur":formateur})

@permission_required('formateur.view_formateur', raise_exception=True)
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

@permission_required('apprenant.view_apprenant', raise_exception=True)
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

@permission_required('apprenant.add_apprenant', raise_exception=True)
def create_apprenant(request):
    form = formulaire.ApprenantForm()
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

@permission_required('apprenant.change_apprenant', raise_exception=True)
def modifier_apprenant(request, id):
    apprenant = Apprenant.objects.get(id=id)
    form = formulaire.ApprenantForm(request.POST or None, instance=apprenant)
    if form.is_valid():
        form.save()
        return redirect("/liste_apprenant/")
    return render(request, "utilisateur/modifier_apprenant.html", {"apprenant": apprenant, "form":form})


@login_required
def info_utilisateur(request):
    utilisateur = request.user
    #on vérifie si l'utilisateur connecté est un formateur ou apprenant ou admin
    try: 
        info_app = Apprenant.objects.get(user_apprenant_id=utilisateur)
        return render(request,"utilisateur/info_app.html", {"info_app":info_app})
    except Apprenant.DoesNotExist:
        pass
    try:
        
        info_form = Formateur.objects.get(user_formateur_id=utilisateur)
        

        # on récupère les emplois du temps du formateur
        planning = Planning.objects.filter(formateur=info_form)

        # on extrait les classes associées au formateur connecté à travers son emploi du temps
        mes_classes = set(emploi.classe for emploi in planning)
            
            
        return render(request, "utilisateur/info_formateur.html", {"info_form":info_form, "mes_classes":mes_classes})

    except Formateur.DoesNotExist:
        pass
    #si l'utilisateur n'est un formateur, il vérifie si est appprenant
    
    if request.user.is_superuser:
            
        return render(request,"utilisateur/tableau_admin.html")
    return render(request,"utilisateur/error.html")
        


@login_required
def info_planning(request, id):
    planning = get_object_or_404(Planning, id=id) 
    return render(request, "planning/info_planning.html", {"planning":planning})

 

@login_required
@permission_required('matiere.view_matiere', raise_exception=True)
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

@login_required
@permission_required('matiere.change_matiere', raise_exception=True)
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

@login_required
@permission_required('matiere.delete_matiere', raise_exception=True)
def supprimer_matiere(request, id):
    matiere = get_object_or_404(Matiere, id=id)
    
    matiere = Matiere.objects.filter(pk=id)
    matiere.update(
        archive=True
    )
    return redirect("/liste_matiere/")
    
#tableau bord administrateur
def tableau_admin(request):
    return render(request, "utilisateur/tableau_admin.html")



#lister les filiere
def list_filiere(request):
    filieres = Filiere.objects.all()
    return render(request, "utilisateur/liste_filiere.html", {"filieres":filieres})

#les envoies mails
def send_emails(request):
    if request.method == "POST":
        form = formulaire.SendEmailForm(request.POST)
    
        if form.is_valid():
            users = form.cleaned_data['users']
            sujet = form.cleaned_data['sujet']
            message = form.cleaned_data['message']
            for user in users:
                send_mail(
                    sujet,
                    message,
                    'settings.EMAIL_HOST_USER',
                    [user.email],
                    fail_silently=False,

                )
                messages.success(request, "les mails sont envoyés avec success")
                return redirect("/tableau_administrateur/")
    else:
        form = formulaire.SendEmailForm()
    return render(request, "planning/send_email.html", {"form":form})
