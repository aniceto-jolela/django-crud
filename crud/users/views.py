from django.shortcuts import render, redirect
from .forms import UserRegister
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'users/home.html', {'title':'Home'})


def about(request):
    return render(request, 'users/about.html',{'title':'About'})


def register(request):
    if request.method == 'POST':
        form = UserRegister(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, f'{user} created successful.')
            return redirect('home')
    else:
        form = UserRegister()
    return render(request, 'users/register.html', {'form':form})


@login_required
def profile(request):
    return render(request, 'users/profile.html', {'title': 'Profile'})


