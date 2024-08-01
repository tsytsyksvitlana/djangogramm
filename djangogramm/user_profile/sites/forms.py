from django.contrib.auth.forms import UserChangeForm
from django import forms

from user_profile.models.user import User


class CustomUserChangeForm(UserChangeForm):
    avatar = forms.ImageField(required=False, widget=forms.FileInput(
        attrs={'class': 'form-control-file'}))

    class Meta:
        model = User
        fields = ("username", "email", "bio", "avatar")
