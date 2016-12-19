from django.shortcuts import render, redirect

from .forms import AssessorForm


def register_assessor(request):
    if request.method == 'POST':
        form = AssessorForm(request.POST)
        if form.is_valid():
            return redirect('home')
    else:
        form = AssessorForm()

    return render(request, 'myapp/signup.html', {'form': form})
