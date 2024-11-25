from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from cloudinary.forms import CloudinaryFileField
from .models import Profile


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
    image = CloudinaryFileField()

    class Meta:
        model = Profile
        fields = ['image']


class UserSelectionForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['user', 'image']
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].queryset = User.objects.all() # Use to filter data
