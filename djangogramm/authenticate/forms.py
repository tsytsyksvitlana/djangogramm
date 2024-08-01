from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate


from user_profile.models import User


class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password_confirm = forms.CharField(
        label='Confirm Password', widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        if password != password_confirm:
            raise forms.ValidationError(
                'Password and confirm password does not match.'
            )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.password = make_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        user = authenticate(
            request=self.request, username=username, password=password
        )

        if not user:
            raise forms.ValidationError('Invalid username or password.')
        elif not user.is_active:
            raise forms.ValidationError('This account is inactive.')

        return cleaned_data
