from django import forms
from django.forms import ModelForm

from .models import Address, CustomUser, Profile
from .utils import placeholderify


@placeholderify
class CustomUserForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput()
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['gender', 'picture']


@placeholderify
class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['country', 'postcode', 'state', 'city']


@placeholderify
class LoginForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'password']
        widgets = {
            'password': forms.PasswordInput()
        }
