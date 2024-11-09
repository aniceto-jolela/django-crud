from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Profile
from crispy_forms_foundation.layout import Layout, Fieldset, Field
from crispy_forms.helper import FormHelper


class UserRegister(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser']


class UserUpdate(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class UserFile(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']
