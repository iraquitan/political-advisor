from django.shortcuts import render, redirect

from .forms import AssessorForm, LoginForm


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
    title = "Login Assessor"
    submit = "Login"
    return render(request, 'myapp/form.html', {'form': form, 'title': title,
                                               'submit': submit})


def register_assessor(request):
    if request.method == 'POST':
        form = AssessorForm(request.POST)
        if form.is_valid():
            return redirect('home')
    else:
        form = AssessorForm()
    title = "Register Assessor"
    submit = "Register"
    return render(request, 'myapp/form.html', {'form': form, 'title': title,
                                               'submit': submit})
