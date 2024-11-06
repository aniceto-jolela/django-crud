from django.shortcuts import render, redirect
from .forms import UserRegister, UserUpdate, UserFile
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import (
    UpdateView,
    DetailView
)
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy


def home(request):
    return render(request, 'users/home.html', {'title': 'Home'})


def about(request):
    return render(request, 'users/about.html', {'title': 'About'})


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


def users(request):
    context = {'users_': User.objects.all()}
    return render(request, 'users/user_table.html', context)


class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    # <app>/<model>_<viewtype>.html
    model = User
    template_name = 'users/user_form.html'
    fields = ['username', 'email']
    success_url = reverse_lazy('users') # Redirect to a profile page or wherever appropriate

    def form_valid(self, form):
        form.instance.username = form.cleaned_data.get('username')
        form.instance.email = form.cleaned_data.get('email')
        return super().form_valid(form)

    def test_func(self):
        # Ensure that only the user can update their own profile
        user = self.get_object()
        return self.request.user == user


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'users/user_detail.html'
