from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.views import View
from django.views.generic import DetailView
from django.views.generic.edit import FormView
from django.shortcuts import render, reverse

from .forms import SignUpForm


# Create your views here.


class LoginView(View):

    def get(self, request):
        return render(request, 'accounts/login.html')


class SignupView(FormView):
    form_class = SignUpForm
    template_name = 'accounts/register.html'

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password2')
        username = email.split('@')[0]
        form.cleaned_data.update({
            'username': username,
            'is_staff': True,
            'is_superuser': True
        })
        form.save()
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return HttpResponse(
            reverse('dashboard')
        )


class ProfileView(DetailView):
    model = User


class DashboardView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'base.html')
