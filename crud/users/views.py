from django.shortcuts import render


def home(request):
    return render(request, 'users/home.html', {'title':'Home'})


def about(request):
    return render(request, 'users/about.html',{'title':'About'})


def profile(request):
    return render(request, 'users/profile.html', {'title':'Profile'})