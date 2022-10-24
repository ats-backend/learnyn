import io
import csv
from random import randint

from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User, Permission
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Q
from django.http import HttpResponseForbidden, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, FormView

from .forms import LoginForm, SignUpForm, PasswordForm
from .models import ResetPasswordToken
from classadmins.models import ClassAdmin
from helpers.utils import send_mail, send_password_reset_mail
from school.models import Classroom
from students.models import Student


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
        context['classes'] = Classroom.active_objects.all()
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
            reverse('home')
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
            reverse('home')
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
        return HttpResponseRedirect(
            reverse('accounts:login')
        )


class ProfileView(DetailView):
    model = User


class HomeView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        classrooms = Classroom.active_objects.count()
        class_admins = ClassAdmin.active_objects.count()
        students = Student.active_objects.count()
        context = {
            'all_students': students,
            'all_class_admins': class_admins,
            'all_classrooms': classrooms,
        }
        return render(request, 'index.html', context)


class ResetPasswordView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'accounts/reset_password.html')

    def post(self, *args, **kwargs):
        email = self.request.POST.get("email")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(self.request, "User Does Not Exist !")
            return HttpResponseRedirect(self.request.META.get("HTTP_REFERER"))

        try:
            reset_password = ResetPasswordToken.objects.create(user=user, token=randint(99, 9999))
        except:
            reset_password = ResetPasswordToken.objects.get(user=user)

        context = {
            "user": user,
            "token": reset_password.token
        }

        email_body = {
            "subjects": "Password Reset From Learnyn",
            "recipient": email,
        }

        send_password_reset_mail(email_body, context)

        messages.success(self.request, f"Password Reset Token Sent to {email}")
        return render(self.request, "accounts/validate_password_token.html")


def validate_reset_password_token(request):
    if request.method == "POST":
        token = request.POST["token"]

        try:
            reset_token = ResetPasswordToken.objects.get(token=token)
        except ResetPasswordToken.DoesNotExist:
            messages.error(request, "Token is invalid")
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

        uid = urlsafe_base64_encode(force_bytes(reset_token.user_id))
        return HttpResponseRedirect(reverse("accounts:new_password", args=[uid]))


def new_password(request, uid):
    if request.method == "POST":
        dec_uid = urlsafe_base64_decode(uid)

        try:
            user = User.objects.get(id=dec_uid)
        except User.DoesNotExist:
            messages.error(request, "User Does Not Exist !")
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != "" and len(password1) > 6:
            if password1 == password2:
                user.password = make_password(password1)
                user.save()

                messages.success(request, "Password changed Successfully")
                return HttpResponseRedirect(reverse("accounts:login"))

            messages.error(request, "Passwords Do Not Match !")
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

        messages.error(request, "Password cannot be empty")
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    return render(request, "accounts/set_password.html", {"uid": uid})

