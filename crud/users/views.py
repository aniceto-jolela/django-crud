from django.shortcuts import render, redirect, get_object_or_404, reverse
from .forms import UserRegister, UserUpdate, UserFile, Profile
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.generic import (
    ListView,
    UpdateView,
    DetailView,
    DeleteView
)
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
import os
from django.conf import settings


def home(request):
    return render(request, 'users/home.html', {'title': 'Home'})


def about(request):
    return render(request, 'users/about.html', {'title': 'About'})


def register(request):
    if request.method == 'POST':
        form = UserRegister(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'{user.username} created successfully.')
            return redirect('home')
    else:
        form = UserRegister()
    context = {
        'u_form': form,
        'title': 'Register'
    }
    return render(request, 'users/register.html', context)


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


@login_required
def update_pic(request, pk):
    picture_p = get_object_or_404(Profile, user__id=pk)

    if not request.user.is_superuser:
        messages.error(request, 'You do not have permission to update this profile ')
        return redirect('users')

    # Allow superuser to update the profile picture
    if request.method == 'POST':
        form = UserFile(request.POST, request.FILES, instance=picture_p)
        if form.is_valid():
            form.save()
            messages.success(request, 'The image was successfully updated!')
            return redirect('users')
    else:
        form = UserFile(instance=picture_p)
    context = {
        'title': 'Update_pic',
        'form': form
    }
    return render(request, 'users/update_pic.html', context)


@login_required
def management(request):
    # Local file
    profile_pics_path = os.path.join(settings.MEDIA_ROOT, 'profile_pics')
    media_files = os.listdir(profile_pics_path) # List all files in profiles_pics
    context = {
        'title': 'Management',
        'media_files': media_files,
        'user_files': Profile.objects.all()
    }
    return render(request, 'users/management.html', context)


@login_required
def delete_all_data(request):
    if not request.user.is_superuser:
        messages.error(request, 'You do not have permission to delete all Users and Profiles.')
        return redirect('management')

    # Allow superuser to delete all data
    if request.method == 'POST':
        profile_pics_path = os.path.join(settings.MEDIA_ROOT, 'profile_pics')
        if os.path.exists(profile_pics_path):
            if not os.listdir(profile_pics_path):
                messages.warning(request, 'No images found.')
                return redirect('management')
            for filename in os.listdir(profile_pics_path):
                file_path = os.path.join(profile_pics_path, filename)
                try:
                    if os.path.isfile(file_path):
                        os.remove(file_path) # Delete the file
                except Exception as e:
                    messages.error(request, f'Error deleting {filename}: {e}')
        else:
            messages.error(request, 'Directory does not exist.')

        # Profile.objects.all().delete() # Deletes all profiles
        # User.objects.all().delete() # Deletes all users
        messages.success(request, 'All user and profile data were successfully deleted!')
        return redirect('home')
    else:
        return render(request, 'users/delete_all_data.html')


class UserListView(LoginRequiredMixin, ListView):
    model = User
    context_object_name = 'users_'
    template_name = 'users/user_table.html'


class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    # <app>/<model>_<viewtype>.html
    model = User
    template_name = 'users/user_form.html'
    fields = ['username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser']
    success_url = reverse_lazy('users') # Redirect to a profile page or wherever appropriate

    def get_object(self, queryset=None):
        user_id = self.kwargs.get('pk')
        return get_object_or_404(User, pk=user_id)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Restrict fields for non - superusers
        if not self.request.user.is_superuser:
            # Remove sensitive fields from the  form for non-superusers
            form.fields.pop('is_active', None)
            form.fields.pop('is_staff', None)
            form.fields.pop('is_superuser', None)
        return form

    def form_valid(self, form):
        form.instance.username = form.cleaned_data.get('username')
        form.instance.email = form.cleaned_data.get('email')
        messages.success(self.request, 'The user has been successfully updated!')
        return super().form_valid(form)

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        # Ensure that only the user can update their own profile
        user = self.get_object()
        return self.request.user == user


class UserDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = User
    template_name = 'users/user_detail.html'

    def get_object(self, queryset=None):
        user_id = self.kwargs.get('pk')
        return get_object_or_404(User, pk=user_id)

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        user = self.get_object()
        return self.request.user == user


class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = User
    template_name = 'users/user_confirm_delete.html'
    success_url = reverse_lazy('users')

    def get_object(self, queryset=None):
        user_id = self.kwargs.get('pk')
        return get_object_or_404(User, pk=user_id)

    def test_func(self):
        if self.request.user.is_superuser:
            messages.success(self.request, 'The user has been successfully deleted!')
            return True
        return False
