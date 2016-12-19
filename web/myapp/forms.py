from django import forms
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.models import User


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput()
        }

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for key, field in self.fields.items():
            if isinstance(field.widget, (forms.TextInput, forms.Textarea,
                                         forms.DateInput, forms.DateTimeInput,
                                         forms.TimeInput)):
                field.widget.attrs.update({'placeholder': field.label,
                                           'class': 'form-control'})


class LoginForm(ModelForm):
    class Meta:
        model = User
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
