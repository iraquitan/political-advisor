from django import forms
from django.utils.translation import gettext_lazy as _

from ..utils import placeholderify
from ..models.models import AssessorModel, AssessorProfile, Address


@placeholderify
class AssessorForm(forms.ModelForm):
    class Meta:
        model = AssessorModel
        fields = ['first_name', 'last_name', 'username', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput()
        }


class AssessorProfileForm(forms.ModelForm):
    class Meta:
        model = AssessorProfile
        fields = ['gender', 'picture']


@placeholderify
class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['country', 'postcode', 'state', 'city']


@placeholderify
class LoginForm(forms.ModelForm):
    class Meta:
        model = AssessorModel
        fields = ['email', 'password']
        widgets = {
            'password': forms.PasswordInput()
        }
