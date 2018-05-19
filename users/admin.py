from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Profile
from .forms import CustomUserChangeForm, CustomUserCreationForm

# Register your models here.

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Profile)