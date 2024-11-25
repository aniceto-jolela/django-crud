from django.shortcuts import render, redirect, get_object_or_404, reverse
from .forms import UserRegister, UserUpdate, UserFile, Profile, UserSelectionForm
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
import cloudinary.uploader  # Import Cloudinary uploader
from django.contrib.auth.views import LoginView
from django.db import connection
from django.apps import apps
from cloudinary.uploader import destroy


def home(request):
    return render(request, 'users/home.html', {'title': 'Home'})


def about(request):
    return render(request, 'users/about.html', {'title': 'About'})


def register(request):
    if request.method == 'POST':
        form = UserRegister(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                messages.success(request, f'{user.username} created successfully.')
                return redirect('home')
            except Exception as e:
                # Handle the exception gracefully
                messages.error(request, f'An error occurred during registration:  {e}')
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
        if u_form.is_valid():
            try:
                u_form.save()
                user = u_form.cleaned_data.get('username')
                messages.success(request, f'{user} updated successfully!')
                return redirect('users')
            except Exception as e:
                messages.error(request, f'An error occurred during update profile {e}')
    else:
        u_form = UserUpdate(instance=request.user)
    context = {
            'title': 'Profile',
            'u_form': u_form,
        }
    return render(request, 'users/profile.html', context)


@login_required
def update_pic(request, pk):
    user = User.objects.get(pk=pk)  # Get user by ID
    # Check if user is the logged-in user or the superuser
    if request.user != user and not request.user.is_superuser:
        messages.error(request, 'You do not have permission to update this profile')
        return redirect('users')

    profile_user = user.profile  # Access profile through user relationship

    if request.method == 'POST':
        form = UserFile(request.POST, request.FILES, instance=profile_user)
        if form.is_valid():
            # Check if a new image has been uploaded
            if form.cleaned_data['image']:
                form.save()  # Save the form (including the new image)
                # Append the new image URL to the text file
                with open('urls_images.txt', 'a') as f:
                    f.write(f"{form.cleaned_data['image'].url}\n")
                messages.success(request, 'The profile image was successfully updated!')
            return redirect('users')  # Redirect to user management page
    else:
        form = UserFile(instance=profile_user)
    context = {
        'title': 'Update Photo',
        'form': form
    }
    return render(request, 'users/update_pic.html', context)


@login_required
def register_photo_with_user(request):
    if request.method == 'POST':
        form = UserSelectionForm(request.POST, request.FILES)
        if form.is_valid():
            profile_u = form.save()
            # Access the URL from the saved instance
            image_url = profile_u.image.url  # Assuming 'image' is the field for the uploaded file

            # Append the new image URL to the text file
            with open('urls_images.txt', 'a') as f:
                f.write(f"{image_url}\n")
            messages.success(request, f'Profile photo for {profile_u.user} has been uploaded!')
            return redirect('users')  # Redirect to user management page
    else:
        form = UserSelectionForm()
    return render(request, 'users/register_photo_user.html', context={'form': form})


@login_required
def management(request):
    # Local file
    #profile_pics_path = os.path.join(settings.MEDIA_ROOT, 'profile_pics')
    #media_files = os.listdir(profile_pics_path) # List all files in profiles_pics
    with open('urls_images.txt', 'r') as f:
        image_urls = f.readlines()
    context = {
        'title': 'Management',
        'user_files': Profile.objects.all(),
        'image_urls': image_urls
    }
    return render(request, 'users/management.html', context)


@login_required
def delete_all_data(request):
    if not request.user.is_superuser:
        messages.error(request, 'You do not have permission to delete all Users and Profiles.')
        return redirect('management')

    # Allow superuser to delete all data
    # All Files
    if request.method == 'POST':
        # Allow superuser to delete all data
        if request.method == 'POST':
            # Delete all images from Cloudinary
            with open('urls_images.txt', 'r') as f:
                image_urls = f.readlines()

            for image_url in image_urls:
                # Extract the public ID from the image URL (adjust based on your URL format)
                public_id = image_url.strip().split('/')[-1]

                try:
                    destroy(public_id)
                    print(f"Deleted image with public ID: {public_id}")
                except Exception as e:
                    messages.error(request, f"Error deleting image: {e}")
        # Clear the text file
        with open('urls_images.txt', 'w') as f:
            f.truncate()
        messages.success(request, "Images deleted successfully!")

        # Data base
        # Get all models from installed apps
        models = apps.get_models()
        # Clear data and reset IDs for each model
        with connection.cursor() as cursor:
            for model in models:
                # Clear all data from the table
                cursor.execute(f"DELETE FROM {model._meta.db_table};")
                # Reset the auto-incrementing primary key sequence based on the database engine
                if connection.vendor == 'sqlite':
                    cursor.execute(f"DELETE FROM sqlite_sequence WHERE name='{model._meta.db_table}';")
        messages.success(request, 'All data has been successfully reset, and IDs are starting from 1!')
        return redirect('home')
    else:
        return render(request, 'users/delete_all_data.html')


class UserLoginView(LoginView):
    template_name = 'users/login.html'

    def get(self, request, *args, **kwargs):
        # If the user is already authenticated, redirect them to another page
        if request.user.is_authenticated:
            return redirect('home')  # Or the URL where you want to redirect the logged-in user
        return super().get(request, *args, **kwargs)


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

    def form_valid(self, form):
        user = self.get_object()
        profile = getattr(user, 'profile', None)  # Assuming a `Profile` model linked via OneToOneField
        if profile and profile.image:  # Check if the profile has an image
            cloudinary_id = profile.image.public_id  # Replace `public_id` with your field for Cloudinary image ID
            if cloudinary_id:
                # Delete the image from Cloudinary
                cloudinary.uploader.destroy(cloudinary_id)

        # Delete the user
        messages.success(self.request, 'The user has been successfully deleted!')
        return super().form_valid(form)

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        return False
