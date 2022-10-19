from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User, Permission
from django.http import HttpResponseRedirect
from django.views import View
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, FormView
from django.shortcuts import render, reverse

from school.models import Classroom

from .forms import LoginForm, SignUpForm, ClassAdminForm
from .models import ClassAdmin, Student


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


class LogoutView(View):

    def get(self, request):
        logout(request)
        return HttpResponseRedirect(
            reverse('accounts:login')
        )


class SignupView(FormView):
    form_class = SignUpForm
    template_name = 'accounts/register.html'

    def form_valid(self, form):
        permission = Permission.objects.get(
            content_type__model='classadmin',
            name='Can add user'
        )
        email = form.cleaned_data.get('email')
        # password = form.cleaned_data.get('password2')
        username = email.split('@')[0]
        user = form.save()
        user.username = username
        user.is_staff = True
        user.is_superuser = True
        user.user_permissions.add(permission)
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


class ClassAdminDetailView(LoginRequiredMixin, DetailView):
    model = ClassAdmin


class AddClassAdminView(PermissionRequiredMixin, FormView):
    form_class = ClassAdminForm
    template_name = 'accounts/classadmin_form.html'
    permission_required = 'classadmin.can_add_user'

    def form_valid(self, form):
        print(form.cleaned_data)
        classroom_name = form.cleaned_data.pop('classroom')
        email = form.cleaned_data.get('email')
        username = email.split('@')[0]
        class_admin = form.save(username=username)
        classroom = Classroom.objects.filter(name__iexact=classroom_name).first()
        class_admin.classroom.add(classroom)

        return HttpResponseRedirect(
            reverse('class_admins')
        )


class AddStudentView(PermissionRequiredMixin, CreateView):
    model = Student
    permission_required = 'student.can_add_user'
    fields = (
        'first_name',
        'last_name',
        'email',
        'parent_firstname'
        'parent_lastname'
        'parent_email'
    )

    def form_valid(self, form):
        print(form.cleaned_data)
        email = form.cleaned_data.get('email')
        username = email.split('@')[0]
        student = form.save(username=username)
        return HttpResponseRedirect(
            reverse('class_admins')
        )
