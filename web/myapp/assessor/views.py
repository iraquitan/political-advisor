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
    if request.method == 'POST':
        form = AssessorForm(request.POST, prefix='main')
        profile_f = AssessorProfileForm(request.POST, prefix='profile')
        address_f = AddressForm(request.POST, prefix='address')

        if form.is_valid() and profile_f.is_valid():
            print(form.cleaned_data)
            return redirect('home')
    else:
        form = AssessorForm(prefix='main')
        profile_f = AssessorProfileForm(prefix='profile')
        address_f = AddressForm(prefix='address')
    title = _("Register Assessor")
    submit = _("Register")
    return render(request, 'myapp/assessor_form.html',
                  {'form': form, 'profile': profile_f, 'address': address_f,
                   'title': title, 'submit': submit})
