import secrets
import string
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, get_user_model, authenticate
from django.template.loader import render_to_string
from django.urls import reverse
from CourrierProject import settings
from courrier.forms_auth import InscriptionForm, FinalRegistrationForm, ConnexionForm
from courrier.views_notification import get_unread_notifications


def index(request):
    return redirect('auth:connexion')


def dashboard(request, pk):
    # Récupérer l'utilisateur connecté
    user = get_object_or_404(get_user_model(), pk=pk)

    unread_notifications = get_unread_notifications(request)
    unread_notifications_count = unread_notifications.count()
    context = {
        'user': user,
        'unread_notifications': unread_notifications,
        'unread_notifications_count': unread_notifications_count,
    }


    return render(request, 'dashboard.html', context)


def connexion(request):
    if request.method == "POST":
        # Si la requête est une requête POST (formulaire soumis)
        form = ConnexionForm(request.POST)
        if form.is_valid():
            # Si les données du formulaire sont valides
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # Authentifier l'utilisateur avec le nom d'utilisateur et le mot de passe
            user = authenticate(request, username=username, password=password)
            if user is not None:
                # Si l'utilisateur est authentifié avec succès
                login(request, user)
                # Connecter l'utilisateur et le rediriger vers le tableau de bord avec l'ID de l'utilisateur
                return redirect('auth:dashboard', pk=user.pk)
            else:
                # Si l'authentification a échoué
                messages.error(request, 'Adresse e-mail ou mot de passe incorrect.')
    else:
        # Si la requête est une requête GET (affichage du formulaire)
        form = ConnexionForm()
        # Rendre le template 'index.html' avec le formulaire dans le contexte
    return render(request, 'login.html', {'form': form})



def generate_username():
    characters = string.ascii_lowercase + string.digits
    username = ''.join(secrets.choice(characters) for _ in range(12))
    return username


def generate_password():
    characters = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(characters) for _ in range(12))
    return password


def user_register(request):
    if request.method == 'POST':
        form = InscriptionForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = form.cleaned_data['username']
            try:
                # Création de l'utilisateur
                user = User.objects.create_user(username=username, email=email, password=password)

                # Envoi de l'e-mail de confirmation
                final_inscription_url = reverse('auth:user_final_inscription', args=[user.pk])
                email_content = render_to_string('auth/user_mail_register.html', {'user': user, 'password': password, 'final_inscription_url': final_inscription_url})
                send_mail(
                    subject='Confirmation de votre inscription',
                    message='',
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[email],
                    html_message=email_content,
                    fail_silently=False,
                )

                # Affichage d'un message de succès et redirection vers une page de succès
                messages.success(request, f"Votre compte a été créé avec succès. Veuillez consulter votre boîte de réception à l'adresse {email} pour finaliser votre inscription.")
                return redirect(reverse('auth:user_register_success', args=[user.pk]))

            except ValidationError:
                messages.error(request, 'Veuillez entrer une adresse e-mail valide.')
            except Exception as e:
                messages.error(request, 'Une erreur s\'est produite lors de la création de votre compte.')

    else:
        form = InscriptionForm()

    return render(request, 'auth/user_register.html', {'form': form})


def user_register_success(request, pk):
    pk = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        messages.success(request, "Votre mot de passe a été modifié avec succès.")
        return redirect('index', pk=pk)
    return render(request, 'auth/user_register_success.html')


def user_pass_oublie(request):
    return render(request, 'auth/user_pass_oublie.html')


def user_pass_reinit(request):
    return render(request, 'auth/user_pass_reinit.html')


@login_required
def user_final_inscription(request, pk):
    user = get_object_or_404(User, pk=pk)

    if request.method == 'POST':
        form = FinalRegistrationForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save()
            # Authentifier l'utilisateur
            login(request, user)
            # Rediriger vers une page de succès ou effectuer d'autres actions
            return redirect('index')
    else:
        form = FinalRegistrationForm(instance=user)

    return render(request, 'auth/user_final_inscription.html', {'form': form})
