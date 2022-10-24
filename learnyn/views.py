from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View

from classadmins.models import ClassAdmin
from school.models import Classroom
from students.models import Student


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


