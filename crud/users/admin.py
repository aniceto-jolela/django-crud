from django.contrib import admin
from .models import Profile
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


class CustomUserAdmin(UserAdmin):
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not request.user.is_superuser:
            #Disable certain fields for non-superusers
            form.base_fields['is_staff'].disable=True
            form.base_fields['is_superuser'].disable=True
        return form


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Profile)


