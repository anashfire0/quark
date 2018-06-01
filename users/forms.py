from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Profile
from django.core.exceptions import ValidationError
from PIL import Image


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields
        fields += ('email',)

    def clean_username(self):
        return self.cleaned_data['username'].lower()

    def clean_email(self):
        try: 
            self.Meta.model.objects.get(email__iexact=self.cleaned_data['email'])
            raise ValidationError('The email is already registered')
        except self.Meta.model.DoesNotExist:
            return self.cleaned_data['email']


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = CustomUser
        fields = UserChangeForm.Meta.fields

class ProfileForm(forms.Form):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    email = forms.EmailField()
    first_name = forms.CharField(label='First Name', max_length=128, required=False)
    last_name = forms.CharField(label='First Name', max_length=128, required=False)
    phone_no = forms.RegexField(regex=r'^\+?\d{10,12}$', error_messages={"invalid":("Enter a valid number")}, required=False)
    profile_pic = forms.ImageField(required=False)

    def clean_first_name(self):
        return self.cleaned_data['first_name'].title()

    def clean_last_name(self):
        return self.cleaned_data['last_name'].title()

    def save(self):
        self.user.email = self.cleaned_data['email']
        self.user.first_name = self.cleaned_data['first_name']
        self.user.last_name = self.cleaned_data['last_name']
        self.user.profile.phone_no = self.cleaned_data['phone_no']
        self.user.profile.profile_pic = self.cleaned_data['profile_pic']
        self.user.profile.save()
        self.user.save()
        return self.user