from pyexpat import model
from django.contrib.auth.models import Group
from django import forms
from .models import *


class RolesForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ("__all__")

    def __init__(self, *args, **kwargs):
        super(RolesForm, self).__init__(*args, **kwargs)
        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({'class':'form-control form-control-sm'})
