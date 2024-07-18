from django.urls import path
from courrier.views_auth import dashboard, user_register, user_pass_oublie, user_pass_reinit, \
    user_register_success, user_final_inscription, connexion


app_name = 'auth'


urlpatterns = [
    path('connexion/', connexion, name='connexion'),
    path('dashboard/<int:pk>/', dashboard, name='dashboard'),
    path('user_final_inscription/<int:pk>/', user_final_inscription, name='user_final_inscription'),
    path('inscription/', user_register, name='user_register'),
    path('user_pass_oublie/', user_pass_oublie, name='user_pass_oublie'),
    path('user_register_success/<int:pk>/', user_register_success, name='user_register_success'),
    path('user_pass_reinit/', user_pass_reinit, name='user_pass_reinit'),
]
