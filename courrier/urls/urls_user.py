from django.urls import path


from courrier.views_user import (
    utilisateur_list,
    utilisateur_invitation,
    utilisateur_detail,
    utilisateur_create,
    utilisateur_update,
    utilisateur_delete,
    employer_list,
    employer_detail,
    employer_create,
    employer_update,
    employer_delete, search_users, utilisateur_affectation
)

app_name = 'user'

urlpatterns = [
    path('utilisateur_list/', utilisateur_list, name='utilisateur_list'),
    path('utilisateur/<int:pk>/', utilisateur_detail, name='utilisateur_detail'),
    path('utilisateur/new/', utilisateur_create, name='utilisateur_create'),
    path('utilisateur/invite/', utilisateur_invitation, name='utilisateur_invitation'),
    path('utilisateur/<int:pk>/edit/', utilisateur_update, name='utilisateur_update'),
    path('utilisateur/<int:pk>/delete/', utilisateur_delete, name='utilisateur_delete'),
    path('user/utilisateur/<int:user_id>/affectation/', utilisateur_affectation, name='utilisateur_affectation'),

    path('employer_list', employer_list, name='employer_list'),
    path('<int:pk>/', employer_detail, name='employer_detail'),
    path('new/', employer_create, name='employer_create'),
    path('<int:pk>/edit/', employer_update, name='employer_update'),
    path('<int:pk>/delete/', employer_delete, name='employer_delete'),

    path('search/', search_users, name='search_users'),
]