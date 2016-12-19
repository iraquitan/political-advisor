from django.shortcuts import render, redirect
from redis import Redis

from .forms import UserForm, LoginForm

redis = Redis(host='redis', port=6379)


# Create your views here.
def home(request):
    context = dict()
    counter = redis.incr('counter')
    context['counter'] = counter
    return render(request=request, template_name='myapp/home.html',
                  context=context)


def signup(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = UserForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # redirect to a new URL:
            return redirect('home')

            # if a GET (or any other method) we'll create a blank form
    else:
        form = UserForm()
    title = "Sign Up"
    submit = "Register"
    return render(request, 'myapp/form.html', {'form': form, 'title': title,
                                               'submit': submit})


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
    title = "Login"
    submit = "Login"
    return render(request, 'myapp/form.html', {'form': form, 'title': title,
                                               'submit': submit})
