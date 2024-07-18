from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Notification, DestinataireNotification


@login_required
def notifications_list(request):
    """
    Affiche la liste des notifications de l'utilisateur connecté.
    """
    employer = request.user.employer
    notifications = DestinataireNotification.objects.filter(destinataire=employer)
    return render(request, 'notification/notifications_list.html', {'notifications': notifications})

@login_required
def notification_detail(request, pk):
    """
    Affiche les détails d'une notification spécifique.
    """
    employer = request.user.employer
    notification = get_object_or_404(DestinataireNotification, pk=pk, destinataire=employer)
    return render(request, 'notification/notification_detail.html', {'notification': notification})


@login_required
def marquer_comme_lue(request, pk):
    """
    Marque une notification comme lue pour l'utilisateur connecté.
    """
    employer = request.user.employer
    notification = get_object_or_404(DestinataireNotification, pk=pk, destinataire=employer)
    notification.notification.lue = True
    notification.notification.save()
    return redirect('notification:notifications_list')



@login_required
def get_unread_notifications(request):
    employer = request.user.employer
    unread_notifications = DestinataireNotification.objects.filter(
        destinataire=employer,
        notification__lue=False
    ).order_by('-notification__date_creation')
    return unread_notifications