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
        form = AssessorForm(request.POST, prefix='ass_f')
        prof_form = AssessorProfileForm(request.POST, prefix='ass_f')
        address_form = AddressForm(request.POST, prefix='add_f')
        if form.is_valid():
            return redirect('home')
    else:
        assessor_form = AssessorForm(prefix='ass_f')
        prof_form = AssessorProfileForm(prefix='ass_f')
        address_form = AddressForm(prefix='add_f')
    title = _("Register Assessor")
    submit = _("Register")
    return render(request, 'myapp/assessor_form.html',
                  {'form': assessor_form, 'profile': prof_form,
                   'address': address_form, 'title': title, 'submit': submit})
