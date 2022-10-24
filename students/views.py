import io
import csv
from random import randint

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User, Permission
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Q
from django.http import HttpResponseForbidden, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, reverse
from django.views import View
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, FormView

from students.forms import StudentForm
from accounts.views import ClassroomMixin
from classadmins.models import ClassAdmin
from students.models import Student
from helpers.utils import send_mail, send_password_reset_mail
from school.models import Classroom

# Create your views here.


class AddStudentView(ClassroomMixin, LoginRequiredMixin, UserPassesTestMixin, FormView):
    form_class = StudentForm
    template_name = 'students/add_student_form.html'

    def test_func(self):
        return self.request.user.is_superuser or self.is_class_admin

    def form_valid(self, form):
        if self.request.user.is_superuser:
            classroom_id = form.cleaned_data.get('classroom').id
        else:
            class_admin = ClassAdmin.objects.filter(id=self.request.user.id).first()
            classroom_id = class_admin.classroom.id
        student = Student.objects.create(
            classroom_id=classroom_id,
            **form.cleaned_data
        )
        subject = "Welcome to Learnyn, your new student account is ready"
        password_url = reverse('accounts:set-password', args=[student.id])
        action_url = str(get_current_site(self.request)) + password_url
        send_mail(
            receiver=student,
            subject=subject,
            action_url=action_url
        )

        return HttpResponseRedirect(
            reverse('students:students')
        )


class StudentListView(ClassroomMixin, LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Student
    template_name = 'students/student_list.html'
    paginate_by = 12

    def test_func(self):
        return self.request.user.is_superuser or self.is_class_admin

    def get_queryset(self):
        if self.request.user.is_superuser:
            if self.request.GET.get('query'):
                search_query = self.request.GET.get('query')
                return Student.objects.filter(
                    Q(first_name__icontains=search_query) |
                    Q(last_name__icontains=search_query) |
                    Q(classroom__name__icontains=search_query)
                )
            elif self.request.GET.get('classroom'):
                classroom_id = self.request.GET.get('classroom')
                return Student.objects.filter(
                    classroom_id=classroom_id
                )

            elif self.request.GET.get('is_suspended'):
                is_suspended = self.request.GET.get('is_suspended')
                return Student.objects.filter(
                    is_suspended=is_suspended
                )
            return Student.objects.all()

        class_admin = ClassAdmin.objects.filter(id=self.request.user.id).first()

        if self.request.GET.get('query'):
            search_query = self.request.GET.get('query')
            return class_admin.classroom.students(manager='objects').filter(
                Q(first_name__icontains=search_query) |
                Q(last_name__icontains=search_query) |
                Q(classroom__name__icontains=search_query)
            )

        elif self.request.GET.get('classroom'):
            classroom_id = self.request.GET.get('classroom')
            return class_admin.classroom.students(manager='objects').filter(
                classroom_id=classroom_id
            )

        elif self.request.GET.get('is_suspended'):
            is_suspended = self.request.GET.get('is_suspended')
            return class_admin.classroom.students(manager='objects').filter(
                is_suspended=is_suspended
            )
        return class_admin.classroom.students.all()

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data()
    #     if self.request.GET.get('query'):
    #         search_query = self.request.GET.get('query')
    #         context['student_list'] = Student.objects.filter(
    #             Q(first_name__icontains=search_query) |
    #             Q(last_name__icontains=search_query) |
    #             Q(classroom__name__icontains=search_query)
    #         )
    #     if self.request.GET.get('classroom'):
    #         classroom_id = self.request.GET.get('classroom')
    #         context['student_list'] = Student.objects.filter(
    #             classroom_id=classroom_id
    #         )
    #     if self.request.GET.get('is_suspended'):
    #         is_suspended = self.request.GET.get('is_suspended')
    #         context['student_list'] = Student.objects.filter(
    #             is_suspended=is_suspended
    #         )
    #     return context


class StudentDetailView(ClassroomMixin, LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Student
    template_name = 'students/student_detail.html'

    def test_func(self):
        return self.request.user.is_superuser or self.is_class_admin or self.is_student


class UploadStudentView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        student_raw_file = request.FILES.get('student_file')
        student_file = student_raw_file.read().decode('utf-8')
        class_admin = ClassAdmin.objects.filter(id=request.user.id).first()
        for data in csv.DictReader(io.StringIO(student_file)):
            student = Student.objects.create(classroom=class_admin.classroom, **data)
            subject = "Welcome to Learnyn, your new student account is ready"
            password_url = reverse('accounts:set-password', args=[student.id])
            action_url = str(get_current_site(self.request)) + password_url
            send_mail(
                receiver=student,
                subject=subject,
                action_url=action_url
            )
        return HttpResponseRedirect(
            reverse('students:students')
        )


class SuspendStudent(ClassroomMixin, LoginRequiredMixin, View):

    def test_func(self):
        return self.request.user.is_superuser

    def post(self, request, pk, *args, **kwargs):
        student = Student.objects.filter(id=pk).first()
        student.is_suspended = not student.is_suspended
        student.save()

        return HttpResponseRedirect(
            reverse('students:students')
        )


# class DownloadStudentDataView(View):
#
#     def get(self, request, pk, *args, **kwargs):
#         students = Student.objects.filter(classroom_id=pk)
#         classroom = Classroom.objects.filter(id=pk)
#         with open(rf'learnyn\static\students_subjects_data\{classroom.name}_subjects.csv', 'w') as f:
#             headers = ["student_id", "subjects", "score"]
#             handler = csv.DictWriter(f, fieldnames=headers)
#             handler.writeheader()
#             for student in students:
#                 for subject in student.classroom.subjects.all():
#                     handler.writerows([{
#                         'student_id': student.student_id,
#                         'subjects': subject.name,
#                         'score': ''
#                     }])
#         return
