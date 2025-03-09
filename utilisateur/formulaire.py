from django import forms
from .models import Filiere, User, Formateur,Apprenant
from plannings.models import Classe, Planning


class LoginForm(forms.Form):
    email = forms.EmailField(max_length=63, label='Email', widget=forms.EmailInput(
        attrs={
             "class":"bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-[#095415]  focus:border-[#095415]  block w-full p-2.5 dark:bg-white dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-900 dark:focus:ring-[#095415]  dark:focus:border-[#095415]"
        }
        ))
    password = forms.CharField(max_length=63,  label='Mot de passe', widget=forms.PasswordInput(
        attrs={
             "class":"mb-3 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-[#095415]  focus:border-[#095415]  block w-full p-2.5 dark:bg-white dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-900 dark:focus:ring-[#095415]  dark:focus:border-[#095415]"
        }
        ))
    

class FormateurForm(forms.ModelForm):
    nom = forms.CharField(max_length=200, widget=forms.TextInput(
        attrs={
             "class":"bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-[#095415]  focus:border-[#095415]  block w-full p-2.5 dark:bg-white dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-900 dark:focus:ring-[#095415]  dark:focus:border-[#095415]"
        }
        ))
    prenom = forms.CharField(max_length=200, widget=forms.TextInput(
        attrs={
             "class":"bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-cyan-500 focus:border-cyan-500 block w-full p-2.5 dark:bg-white dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-cyan-500 dark:focus:border-cyan-500"
        }
        ))
    email = forms.EmailField(max_length=63, label='Email', widget=forms.EmailInput(
        attrs={
             "class":"bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-cyan-500 focus:border-cyan-500 block w-full p-2.5 dark:bg-white dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-emerald-900 dark:focus:border-cyan-500"
        }
        ))
    specialite = forms.CharField(max_length=200, widget=forms.TextInput(
        attrs={
             "class":"bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-cyan-500 focus:border-cyan-500 block w-full p-2.5 dark:bg-white dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-cyan-500 dark:focus:border-cyan-500"
        }
        ))
    filiere = forms.ModelMultipleChoiceField(queryset=Filiere.objects.all(), widget=forms.SelectMultiple(
         attrs={
             "class":"bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-cyan-500 focus:border-cyan-500 block w-full p-2.5 dark:bg-white dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-cyan-500 dark:focus:border-cyan-500"
        }
    ))

    user_formateur = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.Select(
        attrs={
             "class":"mb-10 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-cyan-500 focus:border-cyan-500 block w-full p-2.5 dark:bg-white dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-cyan-500 dark:focus:border-cyan-500"
        }
        ))
    class Meta:
        model = Formateur
        fields = ['nom', 'prenom','email','specialite', 'filiere', 'user_formateur']
    


class ApprenantForm(forms.ModelForm):
    nom = forms.CharField(max_length=200, widget=forms.TextInput(
        attrs={
             "class":"bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-cyan-500 focus:border-cyan-500 block w-full p-2.5 dark:bg-white dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-cyan-500 dark:focus:border-cyan-500"
        }
        ))
    prenom = forms.CharField(max_length=200, widget=forms.TextInput(
        attrs={
             "class":"bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-cyan-500 focus:border-cyan-500 block w-full p-2.5 dark:bg-white dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-cyan-500 dark:focus:border-cyan-500"
        }
        ))
    email = forms.EmailField(max_length=63, label='Email', widget=forms.EmailInput(
        attrs={
             "class":"bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-cyan-500 focus:border-cyan-500 block w-full p-2.5 dark:bg-white dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-emerald-900 dark:focus:border-cyan-500"
        }
        ))
    user_apprenant = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.Select(
        attrs={
             "class":"mb-10 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-cyan-500 focus:border-cyan-500 block w-full p-2.5 dark:bg-white dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-cyan-500 dark:focus:border-cyan-500"
        }
        ))
    classe_apprenant = forms.ModelChoiceField(queryset=Classe.objects.all(), widget=forms.Select(
        attrs={
             "class":"mb-10 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-cyan-500 focus:border-cyan-500 block w-full p-2.5 dark:bg-white dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-cyan-500 dark:focus:border-cyan-500"
        }
        ))
    
    class Meta:
        model = Apprenant
        fields = ['nom','prenom','email', 'user_apprenant', 'classe_apprenant']



class PlanningForm(forms.ModelForm):
    class Meta:
        model = Planning
        fields = '__all__'
    
        widgets = {
            'date_debut': forms.DateInput(attrs={ "class":"mb-5 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-cyan-500 focus:border-cyan-500 block w-full p-2.5 dark:bg-white dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-cyan-500 dark:focus:border-cyan-500"}),
            'date_fin': forms.DateInput(attrs={ "class":"mb-5 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-cyan-500 focus:border-cyan-500 block w-full p-2.5 dark:bg-white dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-cyan-500 dark:focus:border-cyan-500"}),
            'jour': forms.Select(attrs={ "class":"mb-5 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-cyan-500 focus:border-cyan-500 block w-full p-2.5 dark:bg-white dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-cyan-500 dark:focus:border-cyan-500"}),
            'heure_cours': forms.TextInput(attrs={ "class":"mb-5 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-cyan-500 focus:border-cyan-500 block w-full p-2.5 dark:bg-white dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-cyan-500 dark:focus:border-cyan-500"}),
            'classe': forms.Select(attrs={ "class":"mb-5 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-cyan-500 focus:border-cyan-500 block w-full p-2.5 dark:bg-white dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-cyan-500 dark:focus:border-cyan-500"}),
            'duree': forms.TextInput(attrs={ "class":"mb-5 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-cyan-500 focus:border-cyan-500 block w-full p-2.5 dark:bg-white dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-cyan-500 dark:focus:border-cyan-500"}),
            'formateur': forms.Select(attrs={ "class":"mb-5 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-cyan-500 focus:border-cyan-500 block w-full p-2.5 dark:bg-white dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-cyan-500 dark:focus:border-cyan-500"}),
            'matiere': forms.Select(attrs={ "class":"mb-5 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-cyan-500 focus:border-cyan-500 block w-full p-2.5 dark:bg-white dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-cyan-500 dark:focus:border-cyan-500"}),
            'salle': forms.Select(attrs={ "class":"mb-5 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-cyan-500 focus:border-cyan-500 block w-full p-2.5 dark:bg-white dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-cyan-500 dark:focus:border-cyan-500"}),
            
        }
    
class DateEdtForm(forms.Form):
    date_debut = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', "class":"border border-gray-500 rounded-lg"}))
    date_fin = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', "class":"border border-gray-500 rounded-lg"}))

class DateEdtFormateurForm(forms.Form):
    date_debut = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', "class":"mb-2 border border-gray-500 rounded-lg"}))
    date_fin = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', "class":"mb-2 border border-gray-500 rounded-lg"}))
    classe = forms.ModelChoiceField(queryset=Classe.objects.all(), widget=forms.Select(attrs={"class":"mb-2 border border-gray-500 rounded-lg"}))

class SendEmailForm(forms.Form):
    users = forms.ModelMultipleChoiceField(queryset=User.objects.all(), widget=forms.SelectMultiple(
        attrs={
             "class":"mb-3 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-cyan-500 focus:border-cyan-500 block w-full p-2.5 dark:bg-white dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-cyan-500 dark:focus:border-cyan-500"
        }
        ))
    sujet = forms.CharField(max_length=200, label="Sujet", widget=forms.TextInput(attrs={"class":"mb-3 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-cyan-500 focus:border-cyan-500 block w-full p-2.5 dark:bg-white dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-cyan-500 dark:focus:border-cyan-500"}))
    message = forms.CharField(max_length=300, widget=forms.Textarea(attrs={"class":"mb-5 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-cyan-500 focus:border-cyan-500 block w-full p-2.5 dark:bg-white dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-cyan-500 dark:focus:border-cyan-500"}), label="Message")

    