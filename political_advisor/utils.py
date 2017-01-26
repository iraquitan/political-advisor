import hashlib
import sys

from django import forms

if sys.version_info < (3, 6):
    import sha3


def placeholderify(form):
    class WrappedForm(form):
        def __init__(self, *args, **kwargs):
            super(WrappedForm, self).__init__(*args, **kwargs)
            for key, field in self.fields.items():
                if isinstance(field.widget, (forms.TextInput, forms.Textarea,
                                             forms.DateInput,
                                             forms.DateTimeInput,
                                             forms.TimeInput)):
                    field.widget.attrs.update({'placeholder': field.label,
                                               'class': 'form-control'})
    return WrappedForm


def get_unique_username(obj):
    username = hashlib.sha3_512()
    if obj.user_type == 'AU':
        key_comb = (obj.email.encode('utf-8') +
                    obj.user_type.encode('utf-8') +
                    obj.super_user.username.encode('utf-8'))
    elif obj.user_type == 'SU':
        key_comb = (obj.email.encode('utf-8') +
                    obj.user_type.encode('utf-8') +
                    b'')
    else:
        raise TypeError("'user_type' {obj.user_type} not allowed".format(obj))
    username.update(key_comb)
    return username.hexdigest()
