from django import forms
from courrier.models import Direction, Service, FonctionEmployer, Employer


class DirectionForm(forms.ModelForm):
    class Meta:
        model = Direction
        fields = ['sigle', 'direction', 'logo_dir', 'bp_dir', 'adresse_dir']
        widgets = {
            'direction': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Direction'}),
            'sigle': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Sigle'}),
            'logo_dir': forms.FileInput(),  # Utiliser forms.FileInput() pour un champ ImageField
            'bp_dir': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Boîte Postale'}),
            'adresse_dir': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Adresse'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['logo_dir'].widget.attrs.update({'class': 'form-control-file', 'accept': 'image/*'})



class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['direction_service', 'nom_service', 'tutelle_service']
        widgets = {
            'direction_service': forms.Select(attrs={'class': 'form-control', 'placeholder': 'direction de tutelle'}),
            'nom_service': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Service'}),
            'tutelle_service': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Tutelle du Service'}),
        }


class FonctionEmployerForm(forms.ModelForm):
    class Meta:
        model = FonctionEmployer
        fields = ['service', 'fonction_employer']
        widgets = {
            'fonction_employer': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Fonction'}),
        }


class AffectationEmployerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Sélectionnez le nom complet pour chaque utilisateur
        self.fields['user'].label_from_instance = lambda obj: f"{obj.last_name} {obj.first_name}"

        # Sélectionnez le nom complet pour chaque service
        self.fields['service'].label_from_instance = lambda obj: f"{obj.nom_service}"

        # Sélectionnez le nom de la fonction
        self.fields['fonction_employer'].label_from_instance = lambda obj: f"{obj.fonction_employer}"

    class Meta:
        model = Employer
        fields = ['service', 'user', 'fonction_employer']
        widgets = {
            'service': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Service'}),
            'fonction_employer': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Fonction'}),
            'user': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Nom et Prénoms'}),
        }
