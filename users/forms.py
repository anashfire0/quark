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

class ProfileCreateForm(forms.Form):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    email = forms.EmailField()
    first_name = forms.CharField(label='First Name', max_length=128, required=False)
    last_name = forms.CharField(label='First Name', max_length=128, required=False)
    phone_no = forms.RegexField(regex=r'^\+?\d{10,12}$', error_messages={"invalid":("Enter a valid number")})
    profile_pic = forms.ImageField(required=False)
