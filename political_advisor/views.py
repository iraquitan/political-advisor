import os

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.db import transaction
from django.shortcuts import render, redirect
from django.utils.translation import gettext_lazy as _
from redis import Redis

from .models.models import CustomUser
from .forms import CustomUserForm, LoginForm, ProfileForm

redis = Redis(host=os.environ['REDIS_SERVICE'], port=6379)


# Create your views here.
def home(request):
    context = dict()
    counter = redis.incr('counter')
    context['counter'] = counter
    return render(request=request,
                  template_name='political_advisor/home.html',
                  context=context)


@transaction.atomic
def signup(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        custom_user_form = CustomUserForm(request.POST, prefix='main')
        profile_form = ProfileForm(request.POST, prefix='profile')
        # check whether it's valid:
        if all([custom_user_form.is_valid(), profile_form.is_valid()]):
            # process the data in form.cleaned_data as required
            # redirect to a new URL:
            user_data = custom_user_form.cleaned_data
            profile_data = profile_form.cleaned_data
            user = CustomUser.objects.create_user(**user_data)
            # Update user profile
            user.profile.gender = profile_data.get('gender')
            user.profile.picture = profile_data.get('picture')
            user.save()
            messages.success(request, _("Your account was successfully "
                                        "created!"))
            return redirect('home')

            # if a GET (or any other method) we'll create a blank form
    else:
        custom_user_form = CustomUserForm(prefix='main')
        profile_form = ProfileForm(prefix='profile')
    title = _("Sign Up")
    submit = _("Register")
    return render(request, 'political_advisor/assessor_form.html',
                  {'form': custom_user_form, 'profile': profile_form,
                   'title': title, 'submit': submit})


def login_view(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = LoginForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # redirect to a new URL:
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user_type = 'SU'
            user = authenticate(username=email, password=password,
                                user_type=user_type)
            if user is not None:
                login(request, user)
                messages.success(
                    request, _("Welcome {user}").format(user=user.first_name))
                return redirect('home')
            else:
                messages.error(request, _("Login failed, user not found "
                                          "in database!"))
    else:
        form = LoginForm()
    title = _("Login")
    submit = _("Login")
    return render(request, 'political_advisor/form.html',
                  {'form': form, 'title': title, 'submit': submit})
