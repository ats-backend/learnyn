from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User, Permission
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Q
from django.http import HttpResponseForbidden, HttpResponseRedirect, JsonResponse
from django.views import View
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, FormView
from django.shortcuts import render, reverse

from .forms import LoginForm, SignUpForm, ClassAdminForm, PasswordForm, StudentForm
from .models import ClassAdmin, Student
from helpers.utils import send_mail
from school.models import Classroom


# Create your views here.


class ClassroomMixin:

    def dispatch(self, request, *args, **kwargs):
        self.class_admin = ClassAdmin.objects.filter(
            id=request.user.id
        ).first()
        self.is_class_admin = ClassAdmin.objects.filter(
            id=request.user.id
        ).exists()
        self.is_student = Student.objects.filter(
            Q(id=request.user.id) &
            Q(id=self.kwargs.get('pk'))
        ).exists()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['classes'] = Classroom.objects.all()
        return context


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


class SetPasswordView(FormView):
    form_class = PasswordForm
    template_name = 'accounts/set_password.html'

    def form_valid(self, form):
        user_id = self.kwargs.get('pk')
        password = form.cleaned_data.get('password2')
        user = User.objects.filter(id=user_id).first()
        user.set_password(password)
        user.save()


class ProfileView(DetailView):
    model = User


class DashboardView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        return render(request, 'base.html')


class ClassAdminListView(ClassroomMixin, LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = ClassAdmin

    def test_func(self):
        return self.request.user.is_superuser


class ClassAdminDetailView(ClassroomMixin, LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = ClassAdmin

    def test_func(self):
        return self.request.user.is_superuser or self.is_class_admin


class AddClassAdminView(ClassroomMixin, LoginRequiredMixin, UserPassesTestMixin, FormView):
    form_class = ClassAdminForm
    template_name = 'accounts/classadmin_form.html'

    def test_func(self):
        return self.request.user.is_superuser

    def form_valid(self, form):
        classroom_id = form.cleaned_data.pop('classroom')
        class_admin = ClassAdmin.objects.create(
            classroom_id=classroom_id,
            **form.cleaned_data
        )
        subject = "Welcome to Learnyn, your new account is ready"
        password_url = reverse('accounts:set-password', args=[class_admin.id])
        action_url = str(get_current_site(self.request)) + password_url
        send_mail(
            receiver=class_admin,
            subject=subject,
            action_url=action_url
        )

        return HttpResponseRedirect(
            reverse('class_admins')
        )


class AddStudentView(ClassroomMixin, LoginRequiredMixin, UserPassesTestMixin, FormView):
    form_class = StudentForm
    template_name = 'accounts/add_student_form.html'

    def test_func(self):
        return self.request.user.is_superuser or self.is_class_admin

    def form_valid(self, form):
        print(form.cleaned_data)
        class_admin = ClassAdmin.objects.filter(id=self.request.user.id).first()
        if form.cleaned_data.get('classroom'):
            classroom_id = form.cleaned_data.get('classroom').id
        else:
            classroom_id = class_admin.classroom.id
        student = Student.objects.create(
            classroom_id=classroom_id,
            **form.cleaned_data
        )
        id2string = str(student.id).zfill(4)
        student_id = f"LYN-STD-{id2string}"
        student.student_id = student_id
        student.save()
        subject = "Welcome to Learnyn, your new student account is ready"
        password_url = reverse('accounts:set-password', args=[student.id])
        action_url = str(get_current_site(self.request)) + password_url
        send_mail(
            receiver=student,
            subject=subject,
            action_url=action_url
        )

        return HttpResponseRedirect(
            reverse('students')
        )


class StudentListView(ClassroomMixin, LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Student
    template_name = 'accounts/student_list.html'

    def test_func(self):
        return self.request.user.is_superuser or self.is_class_admin

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Student.objects.all()

        class_admin = ClassAdmin.objects.filter(id=self.request.user.id).first()
        return class_admin.classroom.students.all()


class StudentDetailView(ClassroomMixin, LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Student
    template_name = 'accounts/student_detail.html'

    def test_func(self):
        return self.request.user.is_superuser or self.is_class_admin or self.is_student

