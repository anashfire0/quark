from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Profile
from PIL import Image


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields
        fields += ('email',)

    def clean_username(self):
        return self.cleaned_data['username'].lower()


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = CustomUser
        fields = UserChangeForm.Meta.fields

class ProfileCreateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'

    # def clean_profile_pic(self):
    #     try:
    #         size = 512, 512
    #         return Image.open(self.cleaned_data['profile_pic']).thumbnail(size)
    #     except KeyError:
    #         print('ERROR'.center(1000,'%'))

