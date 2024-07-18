from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import CourrierSortant, CourrierEntrant, CourrierSpecialInstruction, CourrierSpecialCopie, Notification, \
    DestinataireNotification, CourrierSpecial, Instruction, Direction, Permission
from courrier.forms_courrier import CourrierSortantForm, CourrierSpecialForm


def courrier_sortant_list(request):
    courriers = CourrierSortant.objects.all()
    return render(request, 'mailbox/mailbox.html', {'courriers': courriers})


@login_required
def courrier_sortant_create(request):
    if request.method == 'POST':
        form = CourrierSortantForm(request.POST, request.FILES)

        if form.is_valid():
            courrier_sortant = form.save(commit=False)
            courrier_sortant.superieur_validation = request.user.employer
            courrier_sortant.save()

            # Copier le courrier sortant dans courrier entrant
            CourrierEntrant.objects.create(
                expediteur=courrier_sortant.expediteur,
                destinataire=courrier_sortant.destinataire,
                sujet=courrier_sortant.sujet,
                contenu=courrier_sortant.contenu,
                joint=courrier_sortant.joint
            )

            # Envoyer une notification au destinataire
            destinataire = courrier_sortant.destinataire
            notification_contenu = f'Vous avez reçu un nouveau courrier de la part de {courrier_sortant.expediteur.user.get_full_name()}.'
            notification = Notification.objects.create(
                direction=destinataire.service.direction_service,
                type='Nouveau Courrier',
                objet_id=courrier_sortant.id,
                contenu=notification_contenu,
                utilisateur=destinataire.user
            )
            DestinataireNotification.objects.create(
                direction=destinataire.service.direction_service,
                notification=notification,
                destinataire=destinataire
            )

            messages.success(request, 'Courrier envoyé avec succès.')
            return redirect('courrier:courrier_sortant_list')
    else:
        form = CourrierSortantForm()

    directions = Direction.objects.all()
    return render(request, 'courrier/courrier_sortant_form.html', {'form': form, 'directions': directions})



def courrier_sortant_detail(request, pk):
    courrier = get_object_or_404(CourrierSortant, pk=pk)
    return render(request, 'courrier/courrier_entrant_detail.html', {'courrier': courrier})



def courrier_sortant_delete(request, pk):
    courrier = get_object_or_404(CourrierSortant, pk=pk)
    if request.method == 'POST':
        courrier.delete()
        return redirect('courrier_sortant_list')
    return render(request, 'courrier/courrier_sortant_list.html', {'courrier': courrier})




def courrier_entrant_list(request):
    courriers = CourrierEntrant.objects.all()
    return render(request, 'courrier/courrier_entrant_list.html', {'courriers': courriers})


def courrier_entrant_detail(request, pk):
    courrier = get_object_or_404(CourrierEntrant, pk=pk)
    return render(request, 'courrier/courrier_entrant_detail.html', {'courrier': courrier})


def courrier_entrant_delete(request, pk):
    courrier = get_object_or_404(CourrierEntrant, pk=pk)
    if request.method == 'POST':
        courrier.delete()
        return redirect('courrier:courrier_entrant_list')
    return render(request, 'courrier/courrier_entrant_list.html', {'courrier': courrier})



def courrier_special_list(request):
    courriers = CourrierSpecial.objects.all()
    return render(request, 'courrier/courrier_special_list.html', {'courriers': courriers})

@login_required
def courrier_special_create(request):
    instructions = Instruction.objects.all()
    directions = Direction.objects.all()

    if request.method == 'POST':
        form = CourrierSpecialForm(request.POST, request.FILES)
        if form.is_valid():
            courrier_special = form.save(commit=False)
            courrier_special.expediteur = request.user.employer  # Associe l'employé connecté comme expéditeur
            courrier_special.save()

            instructions_selected = request.POST.getlist('instructions')
            for instruction_id in instructions_selected:
                courrier_instruction = CourrierSpecialInstruction.objects.create(
                    instruction_id=instruction_id,
                    courrier_special=courrier_special
                )
                directions_selected = request.POST.getlist(f'directions_{instruction_id}')
                for direction_id in directions_selected:
                    CourrierSpecialCopie.objects.create(
                        courrier_special=courrier_special,
                        direction_concerne_id=direction_id
                    )

            # Envoyer une notification au destinataire
            destinataire = courrier_special.destinataire
            notification_contenu = f'Vous avez reçu un nouveau courrier de la part de {courrier_special.expediteur.user.get_full_name()}.'
            notification = Notification.objects.create(
                direction=destinataire.direction_service,
                type='Nouveau Courrier',
                objet_id=courrier_special.id,
                contenu=notification_contenu,
                utilisateur=destinataire.user
            )
            DestinataireNotification.objects.create(
                direction=destinataire.direction_service,
                notification=notification,
                destinataire=destinataire
            )
            messages.success(request, 'Courrier envoyé avec succès.')

            create_notifications(courrier_special)
            return redirect('courrier:courrier_special_list')
    else:
        form = CourrierSpecialForm()

    return render(request, 'courrier/courrier_special_form.html', {
        'form': form,
        'instructions': instructions,
        'directions': directions,
    })


def create_notifications(courrier_special):
    notification_contenu = f"Nouveau courrier spécial : {courrier_special.objet}"
    notification = Notification.objects.create(
        direction=courrier_special.destinataire.direction_service,
        type="Nouveau courrier spécial",
        objet_id=courrier_special.id,
        contenu=notification_contenu
    )

    for employer in courrier_special.destinataire.direction_service.employers.all():
        DestinataireNotification.objects.create(
            direction=courrier_special.destinataire.direction_service,
            notification=notification,
            destinataire=employer
        )




def courrier_special_detail(request, pk):
    courrier = get_object_or_404(CourrierSpecialCopie, pk=pk)
    return render(request, 'courrier/courrier_special_detail.html', {'courrier': courrier})



def courrier_special_delete(request, pk):
    courrier = get_object_or_404(CourrierSpecial, pk=pk)
    if request.method == 'POST':
        courrier.delete()
        return redirect('courrier:courrier_special_list')
    return render(request, 'courrier/courrier_special_list.html', {'courrier': courrier})

