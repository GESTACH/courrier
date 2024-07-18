from django import forms
from courrier.models import CourrierEntrant, CourrierSpecial, CourrierSortant, CourrierSpecialInstruction, Direction
from .models import Mission


class CourrierSpecialInstructionForm(forms.ModelForm):
    class Meta:
        model = CourrierSpecialInstruction
        fields = ['instruction', 'directions_concernees']
        widgets = {
            'instruction': forms.Select(),
            'directions_concernees': forms.SelectMultiple(),
        }


class CourrierSortantForm(forms.ModelForm):
    directions_copies = forms.ModelMultipleChoiceField(
        queryset=Direction.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Directions pour copie"
    )

    class Meta:
        model = CourrierSortant
        fields = ['expediteur', 'destinataire', 'sujet', 'contenu', 'joint']
        widgets = {
            'expediteur': forms.TextInput(),
            'destinataire': forms.Select(),
            'sujet': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Objet'}),
            'contenu': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Contenu du courrier'}),
            'joint': forms.FileInput(attrs={'class': 'form-control', 'placeholder': 'Pièce jointe'}),
        }



class CourrierEntrantForm(forms.ModelForm):
    class Meta:
        model = CourrierEntrant
        fields = ['expediteur', 'destinataire', 'sujet', 'contenu', 'joint', 'lu']
        widgets = {
            'expediteur': forms.TextInput(),
            'destinataire': forms.Select(),
            'sujet': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Objet'}),
            'contenu': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Contenu du courrier'}),
            'joint': forms.FileInput(attrs={'class': 'form-control', 'placeholder': 'Pièce jointe'}),
            'lu': forms.CheckboxInput(attrs={'class': 'form-control', 'placeholder': 'lu'})
        }

class CourrierSpecialForm(forms.ModelForm):
    class Meta:
        model = CourrierSpecial
        fields = ['date_reception', 'objet', 'joint', 'note_1', 'note_2', 'lu']
        widgets = {
            'date_reception': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'sujet': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Objet'}),
            'objet': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contenu du courrier'}),
            'note_1': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Note 1'}),
            'note_2': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Note 2'}),
            'joint' : forms.FileInput(attrs={'class': 'form-control', 'placeholder': 'Pièce jointe'}),
            'lu': forms.CheckboxInput(attrs={'class': 'form-control', 'placeholder': 'lu'})
        }




class MissionForm(forms.ModelForm):
    transport = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Transport'}))
    hebergement = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    repas_fourni = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))

    class Meta:
        model = Mission
        fields = ['ordonnateur', 'reference', 'date_mission', 'date_fin_mission', 'objet_mission', 'transport', 'hebergement', 'repas_fourni']
        widgets = {
            'date_mission': forms.DateInput(attrs={'class': 'form-control datepicker', 'placeholder': 'Date de début'}),
            'date_fin_mission': forms.DateInput(attrs={'class': 'form-control datepicker', 'placeholder': 'Date de fin'}),
            'objet_mission': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Objet de la mission'}),
            'reference': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Référence'}),
            'ordonnateur': forms.Select(attrs={'class': 'form-control'}),
        }



