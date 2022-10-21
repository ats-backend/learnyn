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
from django.views import View
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, FormView
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from .forms import LoginForm, SignUpForm, ClassAdminForm, PasswordForm, StudentForm
from .models import ClassAdmin, Student, ResetPasswordToken
from helpers.utils import send_mail, send_password_reset_mail
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
        print("Got called")
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
        print(password)
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


class ClassAdminListView(ClassroomMixin, LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = ClassAdmin
    paginate_by = 12

    def test_func(self):
        return self.request.user.is_superuser

    def get_queryset(self):
        return ClassAdmin.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        if self.request.GET.get('query'):
            search_query = self.request.GET.get('query')
            context['classadmin_list'] = ClassAdmin.objects.filter(
                Q(first_name__icontains=search_query) |
                Q(last_name__icontains=search_query) |
                Q(classroom__name__icontains=search_query)
            )

        if self.request.GET.get('classroom'):
            classroom_id = self.request.GET.get('classroom')
            context['classadmin_list'] = ClassAdmin.objects.filter(
                classroom_id=classroom_id
            )
        if self.request.GET.get('is_suspended'):
            is_suspended = self.request.GET.get('is_suspended')
            context['classadmin_list'] = ClassAdmin.objects.filter(
                is_suspended=is_suspended
            )
        return context


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
            classroom_id=classroom_id.id,
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
    paginate_by = 12

    def test_func(self):
        return self.request.user.is_superuser or self.is_class_admin

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Student.objects.all()

        class_admin = ClassAdmin.objects.filter(id=self.request.user.id).first()
        return class_admin.classroom.students.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        if self.request.GET.get('query'):
            search_query = self.request.GET.get('query')
            context['student_list'] = Student.objects.filter(
                Q(first_name__icontains=search_query) |
                Q(last_name__icontains=search_query) |
                Q(classroom__name__icontains=search_query)
            )
        if self.request.GET.get('classroom'):
            classroom_id = self.request.GET.get('classroom')
            context['student_list'] = Student.objects.filter(
                classroom_id=classroom_id
            )
        if self.request.GET.get('is_suspended'):
            is_suspended = self.request.GET.get('is_suspended')
            context['student_list'] = Student.objects.filter(
                is_suspended=is_suspended
            )
        return context


class StudentDetailView(ClassroomMixin, LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Student
    template_name = 'accounts/student_detail.html'

    def test_func(self):
        return self.request.user.is_superuser or self.is_class_admin or self.is_student


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
        print("heyy")
        dec_uid = urlsafe_base64_decode(uid)

        try:
            user = User.objects.get(id=dec_uid)
        except User.DoesNotExist:
            messages.error(request, "User Does Not Exist !")
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        print(password2)
        print(password1)

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


class SuspendClassAdmin(ClassroomMixin, LoginRequiredMixin, View):

    def test_func(self):
        return self.request.user.is_superuser

    def post(self, request, pk, *args, **kwargs):
        class_admin = ClassAdmin.objects.filter(id=pk).first()
        class_admin.is_suspended = not class_admin.is_suspended
        class_admin.save()

        return HttpResponseRedirect(
            reverse('class_admins')
        )


class SuspendStudent(ClassroomMixin, LoginRequiredMixin, View):

    def test_func(self):
        return self.request.user.is_superuser

    def post(self, request, pk, *args, **kwargs):
        student = Student.objects.filter(id=pk).first()
        student.is_suspended = not student.is_suspended
        student.save()

        return HttpResponseRedirect(
            reverse('students')
        )


class UnassignClassAdmin(ClassroomMixin, LoginRequiredMixin, View):

    def test_func(self):
        return self.request.user.is_superuser

    def post(self, request, pk, *args, **kwargs):
        class_admin = ClassAdmin.objects.filter(id=pk).first()
        class_admin.classroom = None
        class_admin.save()

        return HttpResponseRedirect(
            reverse('class_admins')
        )


class AssignClassAdmin(ClassroomMixin, LoginRequiredMixin, View):

    def test_func(self):
        return self.request.user.is_superuser

    def post(self, request, pk, *args, **kwargs):
        classroom_id = request.POST.get('classroom_id')
        class_admin = ClassAdmin.objects.filter(id=pk).first()
        class_admin.classroom_id = classroom_id
        class_admin.save()

        return JsonResponse({
            'redirect_url': reverse('class_admins')
        })


class DownloadStudentDataView(View):

    def get(self, request, pk, *args, **kwargs):
        students = Student.objects.filter(classroom_id=pk)
        classroom = Classroom.objects.filter(id=pk)
        with open(rf'learnyn\static\students_subjects_data\{classroom.name}_subjects.csv', 'w') as f:
            headers = ["student_id", "subjects", "score"]
            handler = csv.DictWriter(f, fieldnames=headers)
            handler.writeheader()
            for student in students:
                for subject in student.classroom.subjects.all():
                    handler.writerows([{
                        'student_id': student.student_id,
                        'subjects': subject.name,
                        'score': ''
                    }])
        return
