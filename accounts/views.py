from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.views import View
from django.views.generic import DetailView, ListView
from django.views.generic.edit import FormView
from django.shortcuts import render, reverse

from .forms import LoginForm, SignUpForm
from .models import ClassAdmin


# Create your views here.


class LoginView(FormView):
    form_class = LoginForm
    template_name = 'accounts/login.html'

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        username = email.split('@')[0]
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return HttpResponseRedirect(
            reverse('dashboard')
        )


class SignupView(FormView):
    form_class = SignUpForm
    template_name = 'accounts/register.html'

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        # password = form.cleaned_data.get('password2')
        username = email.split('@')[0]
        user = form.save()
        user.username = username
        user.is_staff = True
        user.is_superuser = True
        user.save()
        # user = authenticate(username=username, password=password)
        login(self.request, user)
        return HttpResponseRedirect(
            reverse('dashboard')
        )


class ProfileView(DetailView):
    model = User


class DashboardView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        return render(request, 'base.html')


class ClassAdminListView(LoginRequiredMixin, ListView):
    model = ClassAdmin
