from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from courrier.forms_user import UserForm, EmployerForm, UserAffectationForm
from .models import Employer
import secrets
import string


class USerForm:
    pass


def utilisateur_invitation(request):
    if request.method == 'POST':
        form_invit = UserCreationForm(request.POST, request.FILES)
        if form_invit.is_valid():
            # Générer un mot de passe aléatoire sécurisé
            caracteres = string.ascii_letters + string.digits + string.punctuation

            user = User.objects.create_user(
                email=form_invit.cleaned_data['email'],
                first_name=form_invit.cleaned_data['first_name'],
                last_name=form_invit.cleaned_data['last_name'],
                password=''.join(secrets.choice(caracteres) for i in range(12))
            )
            nom_prenoms = f"{user.first_name} {user.last_name}"
            # Envoi du mail d'invitation
            send_mail(
                'Invitation à créer un compte',
                'Bonjour {}, vous êtes invité à créer votre compte.'.format(user.first_name),
                'from@example.com',
                [user.email],
                fail_silently=False,
            )
            messages.success(request, 'Un mail vient d\'être envoyé à {}'f"{user.first_name} {user.last_name}")
            return redirect('user:utilisateur_list')
    else:
        form_invit = UserCreationForm()
    context = {
        'form_invit': form_invit
    }
    return render(request, 'user/utilisateur_invite.html', context)



def utilisateur_list(request):
    utilisateurs = User.objects.all()
    form = UserAffectationForm()
    return render(request, 'user/utilisateur_list.html', {'utilisateurs': utilisateurs, 'form': form})


def utilisateur_detail(request, pk):
    utilisateurs = get_object_or_404(User, pk=pk)
    return render(request, 'user/utilisateur_detail.html', {'utilisateur': utilisateurs})


def utilisateur_create(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            first_name = user_form.cleaned_data['first_name']
            last_name = user_form.cleaned_data['last_name']
            email = user_form.cleaned_data['email']
            password = user_form.cleaned_data['password']

            # Créer un utilisateur avec les données du formulaire
            user = User.objects.create_user(username=email, first_name=first_name, last_name=last_name, email=email,
                                            password=password)

            # Afficher un message de succès
            messages.success(request, f"L'utilisateur {first_name} {last_name} a été créé avec succès.")

            # Rediriger vers la vue de liste des utilisateurs
            return redirect('list_users')
    else:
        user_form = UserForm()

    return render(request, 'user/utilisateur_list.html', {'user_form': user_form})


def utilisateur_update(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        if user_form.is_valid():
            user_form.save()
            return redirect('user:utilisateur_list', pk=user.pk)
    else:
        user_form = UserForm(instance=user)

    context = {
        'user_form': user_form,
    }
    return render(request, 'user/utilisateur_form.html', context)


def utilisateur_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.delete()
        return redirect('utilisateur_list')
    return render(request, 'user/utilisateur_confirm_delete.html', {'employer': user})

def utilisateur_affectation(request, user_id):
    utilisateur = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        form = UserAffectationForm(request.POST)
        if form.is_valid():
            service = form.cleaned_data['service']
            fonction_employer = form.cleaned_data['fonction_employer']

            # Vérifier si l'utilisateur a déjà une affectation
            try:
                affectation = utilisateur.employer
                # Mettre à jour l'affectation existante
                affectation.service = service
                affectation.fonction_employer = fonction_employer
                affectation.save()
                messages.success(request, f"L'affectation de {utilisateur.get_full_name()} a été mise à jour.")
            except Employer.DoesNotExist:
                # Créer une nouvelle affectation
                Employer.objects.create(user=utilisateur, service=service, fonction_employer=fonction_employer)
                messages.success(request, f"{utilisateur.get_full_name()} a été affecté avec succès.")

            return redirect('user:utilisateur_list')
    else:
        form = UserAffectationForm()

    return render(request, 'user/utilisateur_list.html', {'form': form, 'utilisateur': utilisateur})



def employer_list(request):
    employers = Employer.objects.all()
    return render(request, 'user/employer_list.html', {'employers': employers})


def employer_detail(request, pk):
    employer = get_object_or_404(Employer, pk=pk)
    return render(request, 'user/employer_detail.html', {'employer': employer})


def employer_create(request):
    if request.method == 'POST':
        form = EmployerForm(request.POST)
        if form.is_valid():
            # Vérifier si l'employé existe déjà
            if not Employer.objects.filter(utilisateur_employer=form.cleaned_data['utilisateur_employer']).exists():
                form.save()
                messages.success(request, "L'employé a été créé avec succès.")
                return redirect('user:employer_list')
            else:
                messages.error(request, "Cet employé existe déjà.")
    else:
        form = EmployerForm()
    return render(request, 'user/employer_form.html', {'form': form})


def employer_update(request, pk):
    # Récupérer l'employé à mettre à jour
    employer = get_object_or_404(Employer, pk=pk)

    if request.method == 'POST':
        # Créer une instance du formulaire avec les données de la requête et de l'instance employé
        form = EmployerForm(request.POST, instance=employer)
        if form.is_valid():
            form.save()
            return redirect('user:employer_list') # Rediriger vers la liste des employés après la mise à jour
    else:
        # Créer une instance du formulaire avec l'instance employé actuelle pour pré-remplir les champs
        form = EmployerForm(instance=employer)
    return render(request, 'user/employer_update.html', {'form': form})


def employer_delete(request, pk):
    employer = get_object_or_404(Employer, pk=pk)
    if request.method == 'POST':
        employer.delete()
        return redirect('employer_list')
    return render(request, 'user/employer_list.html', {'employer': employer})



def search_users(request):
    if request.is_ajax():
        query = request.GET.get('query', '')
        users = User.objects.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(email__icontains=query) |
            Q(username__icontains=query)
        )
        data = [
            {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'is_active': user.is_active
            }
            for user in users
        ]
        return JsonResponse(data, safe=False)
    return JsonResponse({'error': 'Request must be AJAX'}, status=400)