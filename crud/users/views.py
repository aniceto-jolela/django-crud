from django.shortcuts import render, redirect
from .forms import UserRegister, UserUpdate, UserFile
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
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdate(request.POST, instance=request.user)
        f_form = UserFile(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and f_form.is_valid():
            u_form.save()
            f_form.save()
            user = u_form.cleaned_data.get('username')
            messages.success(request, f'{user} updated successfully!')
    else:
        u_form = UserUpdate(instance=request.user)
        f_form = UserFile(instance=request.user.profile)
    context = {
            'title': 'Profile',
            'u_form': u_form,
            'f_form': f_form
        }
    return render(request, 'users/profile.html', context)


