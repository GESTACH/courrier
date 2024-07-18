from django import forms
from django.contrib.auth.models import User
from courrier.models import Employer, Service, FonctionEmployer


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password', 'is_active', 'is_staff', 'is_superuser']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Prénoms'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Mot de passe'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-control', 'placeholder': 'Activé'}),
            'is_staff': forms.CheckboxInput(attrs={'class': 'form-control', 'placeholder': 'Administrateur'}),
            'is_superuser': forms.CheckboxInput(attrs={'class': 'form-control', 'placeholder': 'Super Administrateur'})
        }



class EmployerForm(forms.ModelForm):

    class Meta:
        model = Employer
        fields = [
            'service', 'fonction_employer', 'photo_utilisateur', 'sexe', 'contact',
            'adresse', 'residence', 'date_naissance', 'lieu_naissance', 'Nom_pere',
            'nom_mere', 'matricule', 'num_cni', 'date_cni', 'hors_service',
            'vehicule', 'vehicule_immatriculation'
        ]
        widgets = {
            'service': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Service'}),
            'fonction_employer': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Fonction de l\'employer'}),
            'photo_utilisateur': forms.FileInput(),
            'sexe': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Sexe'}),
            'contact': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contact'}),
            'adresse': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Adresse'}),
            'date_naissance': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'residence': forms.Select(attrs={'class': 'form.form-control', 'placeholder': 'Residence'}),
            'lieu_naissance': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Lieu de naissance'}),
            'Nom_pere': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom du père'}),
            'nom_mere': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom de la mère'}),
            'matricule': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'N° matricule'}),
            'num_cni': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'N° CNI'}),
            'date_cni': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'hors_service': forms.CheckboxInput(attrs={'class': 'form-control'}),
            'vehicule': forms.CheckboxInput(attrs={'class': 'form-control'}),
            'vehicule_immatriculation': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'N° Matricule véhicule'}),
        }



class UserAffectationForm(forms.ModelForm):
    class Meta:
        model = Employer
        fields = [
            'service', 'fonction_employer'
        ]
        widgets = {
            'service': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Service'}),
            'fonction_employer': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Fonction de l\'employer'}),

        }