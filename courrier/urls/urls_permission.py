from django.urls import path

from courrier.views_permission import manage_user_permissions, list_permissions, delete_group, edit_group, create_group, \
    list_groups, delete_permission, edit_permission, create_permission

app_name = 'permission'


urlpatterns = [
    path('manage-user-permissions/<int:user_id>/', manage_user_permissions, name='manage_user_permissions'),
    path('permissions/', list_permissions, name='list_permissions'),
    path('permissions/create/', create_permission, name='create_permission'),
    path('permissions/edit/<int:permission_id>/', edit_permission, name='edit_permission'),
    path('permissions/delete/<int:permission_id>/', delete_permission, name='delete_permission'),
    path('groups/', list_groups, name='list_groups'),
    path('groups/create/', create_group, name='create_group'),
    path('groups/edit/<int:group_id>/', edit_group, name='edit_group'),
    path('groups/delete/<int:group_id>/', delete_group, name='delete_group'),
]
