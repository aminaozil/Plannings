from django.contrib.auth.hashers import make_password
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True, max_length=200)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    def save(self, *args, **kwargs):
   
        if self.password and not self.password.startswith(('pbkdf2_sha256$', 'bcrypt$', 'argon2')):
        
            self.password = make_password(self.password)
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.email}"

class Matiere(models.Model):
    nom_matiere = models.CharField(max_length=200)
    

    def __str__(self):
        return f"{self.nom_matiere}"
    


class Filiere(models.Model):
    nom_filiere = models.CharField(max_length=200)
    matiere = models.ManyToManyField(Matiere, related_name="matiere")
    

    def __str__(self):
        return f"{self.nom_filiere}"
    
class Classe(models.Model):
    nom_classe = models.CharField(max_length=200)
    filiere = models.ForeignKey(Filiere, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.nom_classe}"


class Formateur(models.Model):
    nom = models.CharField(max_length=200, null=True)
    prenom = models.CharField(max_length=200, null=True)
    specialite = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    user_formateur = models.OneToOneField(User, on_delete=models.CASCADE)
    filiere = models.ManyToManyField(Filiere, related_name="formateur")
    archive = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user_formateur.last_name} {self.email}"
    

class Apprenant(models.Model):
    nom = models.CharField(max_length=200, null=True)
    prenom = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True)
    user_apprenant = models.OneToOneField(User, on_delete=models.CASCADE)
    classe_apprenant = models.ForeignKey(Classe, on_delete=models.CASCADE)
    archive = models.BooleanField(default=False)
    

    def __str__(self):
        return f"{self.user_apprenant.first_name} {self.email}"


class Salle(models.Model):
    nom_salle = models.CharField(max_length=150)

    def __str__(self):
        return f"{self.nom_salle}"
    

CHOIX_JOUR = ( 
    ("Lundi", "Lundi"), 
    ("Mardi", "Mardi"), 
    ("Mercredi", "Mercredi"), 
    ("Jeudi", "Jeudi"), 
    ("Vendredi", "Vendredi"), 
    ("Samedi", "Samedi"),
)
   
class Planning(models.Model):
    date_debut = models.DateField()
    date_fin = models.DateField()
    jour = models.CharField(max_length=100, choices=CHOIX_JOUR)
    heure_cours = models.TimeField()
    duree = models.CharField(max_length=20)
    classe = models.ForeignKey(Classe, on_delete=models.CASCADE)
    formateur = models.ForeignKey(Formateur, on_delete=models.CASCADE)
    salle = models.ForeignKey(Salle, on_delete=models.CASCADE)
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.date_debut} {self.date_fin}"