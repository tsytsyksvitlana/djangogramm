import typing as t

from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.http import HttpRequest
from django.shortcuts import (
    HttpResponsePermanentRedirect,
    HttpResponseRedirect,
    redirect
)
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView

from authenticate.forms import UserLoginForm, UserRegisterForm


class UserRegisterView(CreateView):
    template_name = 'register.html'
    success_url = reverse_lazy('login')
    form_class = UserRegisterForm


class UserLoginView(LoginView):
    template_name = 'login.html'
    form_class = UserLoginForm


class UserLogoutView(View):
    def get(
        self, request: HttpRequest, *args: t.Any, **kwargs: t.Any
    ) -> HttpResponseRedirect | HttpResponsePermanentRedirect:
        logout(request)
        return redirect('login')


class UserChangePasswordView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'password_change.html'
    success_url = reverse_lazy('login')
