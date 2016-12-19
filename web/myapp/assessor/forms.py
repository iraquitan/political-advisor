from django import forms
from django.utils.translation import gettext_lazy as _

from ..models.models import AssessorModel, AssessorProfile, Address


class AssessorForm(forms.ModelForm):
    class Meta:
        model = AssessorModel
        fields = ['first_name', 'last_name', 'username', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput()
        }

    def __init__(self, *args, **kwargs):
        super(AssessorForm, self).__init__(*args, **kwargs)
        for key, field in self.fields.items():
            if isinstance(field.widget, (forms.TextInput, forms.Textarea,
                                         forms.DateInput,
                                         forms.DateTimeInput,
                                         forms.TimeInput)):
                field.widget.attrs.update({'placeholder': field.label,
                                           'class': 'form-control'})


class AssessorProfileForm(forms.ModelForm):
    class Meta:
        model = AssessorProfile
        fields = ['gender', 'picture']


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['country', 'state', 'city', 'postcode']


class LoginForm(forms.ModelForm):
    class Meta:
        model = AssessorModel
        fields = ['email', 'password']
        widgets = {
            'password': forms.PasswordInput()
        }

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        for key, field in self.fields.items():
            if isinstance(field.widget, (forms.TextInput, forms.Textarea,
                                         forms.DateInput, forms.DateTimeInput,
                                         forms.TimeInput)):
                field.widget.attrs.update({'placeholder': field.label,
                                           'class': 'form-control'})
