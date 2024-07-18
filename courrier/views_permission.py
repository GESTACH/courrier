from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect, get_object_or_404

from .models import EmployerGroup, EmployerPermission, Employer
from courrier.forms_permission import EmployerGroupForm, EmployerPermissionForm


def is_admin(user):
    return user.is_superuser or user.is_staff


@user_passes_test(is_admin)
def manage_user_permissions(request, user_id):
    employer = get_object_or_404(Employer, id=user_id)

    if request.method == 'POST':
        group_ids = request.POST.getlist('groups')
        permission_ids = request.POST.getlist('permissions')

        # Mettre à jour les groupes
        employer.employer_groups.set(group_ids)

        # Mettre à jour les permissions
        employer.employer_permissions.set(permission_ids)

        messages.success(request, f'Les permissions et groupes de {employer.user.username} ont été mis à jour.')
        return redirect('manage_user_permissions', user_id=user_id)

    context = {
        'employer': employer,
        'all_groups': EmployerGroup.objects.all(),
        'all_permissions': EmployerPermission.objects.all(),
    }
    return render(request, 'permission/manage_user_permissions.html', context)



@user_passes_test(is_admin)
def list_permissions(request):
    form = EmployerPermissionForm(request.POST)
    permissions = EmployerPermission.objects.all()
    return render(request, 'permission/list_permissions.html', {'permissions': permissions, 'form':form})


@user_passes_test(is_admin)
def create_permission(request):
    if request.method == 'POST':
        form = EmployerPermissionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Permission créée avec succès.')
            return redirect('list_permissions')
    else:
        form = EmployerPermissionForm()
    return render(request, 'permission/list_permissions.html', {'form': form})


@user_passes_test(is_admin)
def edit_permission(request, permission_id):
    permission = get_object_or_404(EmployerPermission, id=permission_id)
    if request.method == 'POST':
        form = EmployerPermissionForm(request.POST, instance=permission)
        if form.is_valid():
            form.save()
            messages.success(request, 'Permission modifiée avec succès.')
            return redirect('list_permissions')
    else:
        form = EmployerPermissionForm(instance=permission)
    return render(request, 'permission/list_permissions.html', {'form': form, 'permission': permission})

@user_passes_test(is_admin)
def delete_permission(request, permission_id):
    permission = get_object_or_404(EmployerPermission, id=permission_id)
    if request.method == 'POST':
        permission.delete()
        messages.success(request, 'Permission supprimée avec succès.')
        return redirect('list_permissions')
    return render(request, 'permission/list_permissions.html', {'object': permission})


@user_passes_test(is_admin)
def list_groups(request):
    form = EmployerGroupForm(request.POST)
    groups = EmployerGroup.objects.all()
    return render(request, 'permission/list_groups.html', {'groups': groups, 'forms':form})


@user_passes_test(is_admin)
def create_group(request):
    if request.method == 'POST':
        form = EmployerGroupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Groupe créé avec succès.')
            return redirect('list_groups')
    else:
        form = EmployerGroupForm()
    return render(request, 'permission/list_groups.html', {'form': form})


@user_passes_test(is_admin)
def edit_group(request, group_id):
    group = get_object_or_404(EmployerGroup, id=group_id)
    if request.method == 'POST':
        form = EmployerGroupForm(request.POST, instance=group)
        if form.is_valid():
            form.save()
            messages.success(request, 'Groupe modifié avec succès.')
            return redirect('list_groups')
    else:
        form = EmployerGroupForm(instance=group)
    return render(request, 'permission/list_groups.html', {'form': form, 'group': group})

@user_passes_test(is_admin)
def delete_group(request, group_id):
    group = get_object_or_404(EmployerGroup, id=group_id)
    if request.method == 'POST':
        group.delete()
        messages.success(request, 'Groupe supprimé avec succès.')
        return redirect('list_groups')
    return render(request, 'permission/list_groups.html', {'object': group})