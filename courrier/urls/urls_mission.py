from django.urls import path
from courrier.views_mission import create_mission, read_mission, update_mission, delete_mission, list_mission, \
    detail_mission, print_mission

app_name = 'courrier'

urlpatterns = [
    path('missions/', list_mission, name='list_mission'),
    path('missions/create/', create_mission, name='create_mission'),
    path('missions/<int:pk>/', detail_mission, name='detail_mission'),
    path('missions/<int:pk>/update/', update_mission, name='update_mission'),
    path('missions/<int:pk>/delete/', delete_mission, name='delete_mission'),
    path('missions/<int:pk>/print/', print_mission, name='print_mission'),
    path('missions/<int:pk>/read/', read_mission, name='read_mission'),
]

