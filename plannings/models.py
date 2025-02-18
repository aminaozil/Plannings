from django.db import models

class Salle(models.Model):
    nom_salle = models.CharField(max_length=150)
    archive = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nom_salle}"
    
class Classe(models.Model):
    nom_classe = models.CharField(max_length=200)
    filiere = models.ForeignKey("utilisateur.Filiere", on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.nom_classe}"


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
    formateur = models.ForeignKey("utilisateur.Formateur", on_delete=models.CASCADE)
    salle = models.ForeignKey(Salle, on_delete=models.CASCADE)
    matiere = models.ForeignKey("utilisateur.Matiere", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.date_debut} {self.date_fin} {self.classe} {self.formateur.prenom} {self.formateur.nom}"