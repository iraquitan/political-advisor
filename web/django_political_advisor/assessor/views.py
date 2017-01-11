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
    return render(request, 'django_political_advisor/form.html',
                  {'form': form, 'title': title, 'submit': submit})


def register_assessor(request):
    if request.method == 'POST':
        assessor_form = AssessorForm(request.POST, prefix='main')
        profile_form = AssessorProfileForm(request.POST, prefix='profile')
        address_form = AddressForm(request.POST, prefix='address')

        if all([assessor_form.is_valid(), profile_form.is_valid(),
                address_form.is_valid()]):
            new_assessor = assessor_form.save()
            profile = profile_form.save(commit=False)
            address = address_form.save(commit=False)
            new_assessor.profile = profile
            new_assessor.addresses.add(address)
            assessor_form.save_m2m()
            return redirect('home')
    else:
        assessor_form = AssessorForm(prefix='main')
        profile_form = AssessorProfileForm(prefix='profile')
        address_form = AddressForm(prefix='address')

    title = _("Register Assessor")
    submit = _("Register")
    return render(request, 'django_political_advisor/assessor_form.html',
                  {'form': assessor_form, 'profile': profile_form,
                   'address': address_form, 'title': title, 'submit': submit})
