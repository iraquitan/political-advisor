from django import forms
from django.forms import ModelForm

from django.contrib.auth.models import User
from web.myapp.models.models import AssessorModel


class UserForm(ModelForm):
    class Meta:
        model = User

    password = forms.CharField(widget=forms.PasswordInput())


class AssessorForm(ModelForm):
    class Meta:
        model = AssessorModel

    password = forms.CharField(widget=forms.PasswordInput())
