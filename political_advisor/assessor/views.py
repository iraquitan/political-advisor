from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.utils.translation import gettext_lazy as _

from ..forms import CustomUserForm, LoginForm, AddressForm, ProfileForm


def login_view(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = LoginForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # redirect to a new URL:
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request,
                                 _("Welcome {user}").format(user.first_name))
                return redirect('home')
            else:
                messages.error(request, _("Login failed, user not found "
                                          "in database!"))
    else:
        form = LoginForm()
    title = _("Login Assessor")
    submit = _("Login")
    return render(request, 'political_advisor/form.html',
                  {'form': form, 'title': title, 'submit': submit})


def register_assessor(request):
    if request.method == 'POST':
        custom_user_form = CustomUserForm(request.POST, prefix='main')
        profile_form = ProfileForm(request.POST, prefix='profile')
        address_form = AddressForm(request.POST, prefix='address')

        if all([custom_user_form.is_valid(), profile_form.is_valid(),
                address_form.is_valid()]):
            # new_assessor = custom_user_form.save()
            # profile = profile_form.save(commit=False)
            # address = address_form.save(commit=False)
            # new_assessor.profile = profile
            # new_assessor.addresses.add(address)
            # custom_user_form.save_m2m()
            return redirect('home')
    else:
        custom_user_form = CustomUserForm(prefix='main')
        profile_form = ProfileForm(prefix='profile')
        address_form = AddressForm(prefix='address')

    title = _("Register Assessor")
    submit = _("Register")
    return render(request, 'political_advisor/assessor_form.html',
                  {'form': custom_user_form, 'profile': profile_form,
                   'address': address_form, 'title': title, 'submit': submit})
