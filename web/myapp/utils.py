from django import forms


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