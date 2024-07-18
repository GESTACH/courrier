from django import forms
from courrier.models import EmployerPermission, EmployerGroup


class EmployerPermissionForm(forms.ModelForm):
    class Meta:
        model = EmployerPermission
        fields = ['name', 'description', 'codename']


class EmployerGroupForm(forms.ModelForm):
    class Meta:
        model = EmployerGroup
        fields = ['name', 'description']