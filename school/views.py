from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.views.generic import ListView, DetailView, View
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from .models import Classroom, Subject
from .forms import ClassroomForm, SubjectForm
from accounts.models import Student, ClassAdmin
from accounts.views import ClassroomMixin


# Create your views here.

def check_superuser(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("403.html")


class ClassRoomListView(LoginRequiredMixin, ListView):
    model = Classroom
    template_name = "school/classroom_list.html"
    # template_name = "403.html"
    login_url = "accounts:login"

    # queryset = Classroom.active_objects.all()
    # context_object_name = "classrooms"

    def get_context_data(self, **kwargs):
        search = self.request.GET.get("classroom", "")
        context = super(ClassRoomListView, self).get_context_data(**kwargs)
        context["classrooms"] = Classroom.active_objects.filter(
            Q(name__icontains=search) | Q(category__icontains=search)
            | Q(description__icontains=search))
        return context


class ClassRoomDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Classroom
    template_name = "school/classroom_detail.html"
    login_url = "accounts:login"

    def test_func(self, **kwargs):
        return bool(self.request.user.is_superuser or self.request.user.classroom.id == self.kwargs["pk"])

    def get_context_data(self, **kwargs):
        context = super(ClassRoomDetailView, self).get_context_data(**kwargs)
        context["classroom"] = Classroom.active_objects.get(id=self.kwargs["pk"])
        context["students"] = Student.objects.filter(classroom_id=self.kwargs["pk"])
        return context


@login_required(login_url="accounts:login")
def create_subject(request):
    check_superuser(request)

    if request.method == "POST":
        print("hey")
        form = SubjectForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(request, "Subject created successfully")
            return HttpResponseRedirect(reverse("school:subject_list"))

        errors = (form.errors.as_text()).split("*")
        messages.error(request, errors[len(errors) - 1])
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

    return render(request, "school/create_subject.html", {"form": SubjectForm()})


@login_required(login_url="accounts:login")
def update_subject(request, pk):
    check_superuser(request)

    try:
        subject = Subject.active_objects.get(id=pk)
    except Subject.DoesNotExist:
        messages.error(request, "Subject Does Not Exist !")
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

    if request.method == "POST":
        form = SubjectForm(request.POST, instance=subject)

        if form.is_valid():
            form.save()

            messages.success(request, f"{subject.name} updated successfully")
            return HttpResponseRedirect(reverse("school:subject_list"))

        errors = (form.errors.as_text()).split("*")
        messages.error(request, errors[len(errors) - 1])
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    return render(request, "school/create_subject.html", {"form": SubjectForm(instance=subject), "instance": subject})


class DeleteRestoreSubjectView(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = "accounts:login"

    def test_func(self):
        return self.request.user.is_superuser

    def get(self, request, **kwargs):
        try:
            instance = Subject.objects.get(id=kwargs["pk"])
        except Subject.DoesNotExist:
            messages.error(request, "Subject Does Not Exist !")
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

        instance.is_active = not instance.is_active
        instance.save()

        if not instance.is_active:
            for classroom in Classroom.active_objects.all():
                if instance in classroom.subjects.all():
                    classroom.subjects.remove(instance)
                    classroom.save()
            messages.success(request, f"{instance.name} deleted successfully !")
        else:
            messages.error(request, f"{instance.name} restored successfully !")

        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


class CreateClassroomView(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = "accounts:login"

    def test_func(self):
        return self.request.user.is_superuser

    def get(self, request, *args, **kwargs):
        return render(request, "school/create_classroom.html", {"form": ClassroomForm()})

    def post(self, request, *args, **kwargs):
        form = ClassroomForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()

            messages.success(request, f"{request.POST['name']} Created Successfully !")
            return HttpResponseRedirect(reverse("school:create_classroom"))
        errors = (form.errors.as_text()).split("*")
        messages.error(request, errors[len(errors) - 1])
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@login_required(login_url="accounts:login")
def update_classroom(request, pk):
    check_superuser(request)

    try:
        classroom = Classroom.active_objects.get(id=pk)
    except Classroom.DoesNotExist:
        messages.error(request, "Classroom Does Not Exist !")
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

    if request.method == "POST":
        form = ClassroomForm(request.POST, instance=classroom)

        if form.is_valid():
            form.save()

            messages.success(request, f"{classroom.name} updated successfully")
            return HttpResponseRedirect(reverse("school:classroom_details", args=[pk]))
        errors = (form.errors.as_text()).split("*")
        messages.error(request, errors[len(errors) - 1])
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    return render(request, "school/create_classroom.html",
                  {"form": ClassroomForm(instance=classroom), "instance": classroom})


class DeleteRestoreClassroomView(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = "accounts:login"

    def test_func(self):
        return self.request.user.is_superuser

    def get(self, request, **kwargs):
        try:
            instance = Classroom.objects.get(id=kwargs["pk"])
        except Classroom.DoesNotExist:
            messages.error(request, "Classroom Does Not exist")
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

        instance.is_active = not instance.is_active
        instance.save()

        if not instance.is_active:
            messages.error(request, f"{instance.name} deleted successfully !")
        else:
            messages.error(request, f"{instance.name} restored successfully !")
        return HttpResponseRedirect(reverse("school:classroom_list"))


class SubjectsListView(ClassroomMixin, LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Subject
    template_name = "school/subjects_dashboard.html"
    # queryset = Subject.active_objects.all()
    context_object_name = "subjects"
    login_url = "accounts:login"

    def test_func(self):
        return bool(self.request.user.is_superuser or self.is_class_admin)
    
    def get_queryset(self):
        if self.request.user.is_superuser:
            return Subject.active_objects.all()
        class_admin = ClassAdmin.objects.filter(id=self.request.user.id).first()
        return class_admin.classroom.subjects.all()
        
