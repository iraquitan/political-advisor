from django import forms
from django.forms import ModelForm

from django.contrib.auth.models import User
# from .models.models import AssessorModel


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
    password = forms.CharField(widget=forms.PasswordInput())


# class AssessorForm(ModelForm):
#     class Meta:
#         model = AssessorModel
#
#     password = forms.CharField(widget=forms.PasswordInput())
