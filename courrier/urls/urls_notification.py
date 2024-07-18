from django.urls import path

from courrier.views_notification import notifications_list, notification_detail, marquer_comme_lue

app_name = 'courrier'

urlpatterns = [
    path('notifications/', notifications_list, name='notifications_list'),
    path('notification/<int:pk>/', notification_detail, name='notification_detail'),
    path('notification/<int:pk>/marquer-comme-lue/', marquer_comme_lue, name='marquer_comme_lue'),
    # autres URLs...
]