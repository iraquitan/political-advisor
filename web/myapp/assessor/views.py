from django.forms import formset_factory
from django.shortcuts import render, redirect
from django.utils.translation import gettext_lazy as _

from .forms import AssessorForm, LoginForm, AddressForm, AssessorProfileForm


def login(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = LoginForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # redirect to a new URL:
            return redirect('home')

            # if a GET (or any other method) we'll create a blank form
    else:
        form = LoginForm()
    title = _("Login Assessor")
    submit = _("Login")
    return render(request, 'myapp/form.html', {'form': form, 'title': title,
                                               'submit': submit})


def register_assessor(request):
    ProfileFormSet = formset_factory(AssessorProfileForm)
    AddressFormSet = formset_factory(AddressForm)
    if request.method == 'POST':
        form = AssessorForm(request.POST)
        profile_f = ProfileFormSet(request.POST)
        address_f = AddressFormSet(request.POST)

        if all([form.is_valid(), profile_f.is_valid(), address_f.is_valid()]):
            print(form.cleaned_data)
            print(profile_f.cleaned_data)
            print(address_f.cleaned_data)
            return redirect('home')
    else:
        form = AssessorForm()
        profile_f = ProfileFormSet()
        address_f = AddressFormSet()
    title = _("Register Assessor")
    submit = _("Register")
    return render(request, 'myapp/assessor_form.html',
                  {'form': form, 'profile': profile_f, 'address': address_f,
                   'title': title, 'submit': submit})
