from django.contrib.auth.models import User
from django import forms



class ConnexionForm(forms.Form):
    username = forms.CharField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Mot de passe'})
    )



class InscriptionForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Pseudo'
            }
        )
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Adresse email',
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Mot de passe',
            }
        )
    )

    def clean_email(self):
        email = self.cleaned_data['email']
        existing_user = User.objects.filter(email=email).first()
        if existing_user:
            raise forms.ValidationError("Un compte avec cet email existe déjà.")
        return email


class InscriptionFinale(forms.Form):
    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'last_name']


class FinalRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(label='Nouveau mot de passe', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Nouveau mot de passe', 'style': 'width: 100%'}))
    password2 = forms.CharField(label='Confirmer le mot de passe', widget=forms.PasswordInput(attrs={'class': 'form'
                                                                                                              '-control', 'placeholder': 'Confirmer le mot de passe', 'style': 'width: 100%'}))

    class Meta:
        model = User
        fields = ['email', 'last_name', 'first_name']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Adresse email'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Prénom'}),
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Les mots de passe ne correspondent pas.")

        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.is_active = True  # Activer le compte de l'utilisateur

        if commit:
            user.save()

        return user
