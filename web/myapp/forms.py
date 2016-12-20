from django import forms
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.models import User

from .utils import placeholderify


@placeholderify
class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput()
        }


@placeholderify
class LoginForm(ModelForm):
    class Meta:
        model = User
        fields = ['email', 'password']
        widgets = {
            'password': forms.PasswordInput()
        }
