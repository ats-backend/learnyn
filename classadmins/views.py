from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User, Permission
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Q
from django.http import HttpResponseForbidden, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, reverse
from django.views import View
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, FormView

from .forms import ClassAdminForm
from accounts.views import ClassroomMixin
from classadmins.models import ClassAdmin
from helpers.utils import send_mail, send_password_reset_mail
from school.models import Classroom

# Create your views here.


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
    template_name = 'classadmins/classadmin_form.html'

    def test_func(self):
        return self.request.user.is_superuser

    def form_valid(self, form):
        classroom_id = form.cleaned_data.pop('classroom')
        class_admin = ClassAdmin.objects.create(
            classroom_id=classroom_id.id,
            **form.cleaned_data
        )
        subject = "Welcome to Learnyn, your new account is ready"
        password_url = reverse('accounts_api:api_set_password', args=[class_admin.id])
        action_url = str(get_current_site(self.request)) + password_url
        send_mail(
            receiver=class_admin,
            subject=subject,
            action_url=action_url
        )

        return HttpResponseRedirect(
            reverse('classadmins:class_admins')
        )


class SuspendClassAdmin(ClassroomMixin, LoginRequiredMixin, View):

    def test_func(self):
        return self.request.user.is_superuser

    def post(self, request, pk, *args, **kwargs):
        class_admin = ClassAdmin.objects.filter(id=pk).first()
        class_admin.is_suspended = not class_admin.is_suspended
        class_admin.save()

        return HttpResponseRedirect(
            reverse('classadmins:class_admins')
        )


class UnassignClassAdmin(ClassroomMixin, LoginRequiredMixin, View):

    def test_func(self):
        return self.request.user.is_superuser

    def post(self, request, pk, *args, **kwargs):
        class_admin = ClassAdmin.objects.filter(id=pk).first()
        class_admin.classroom = None
        class_admin.save()

        return HttpResponseRedirect(
            reverse('classadmins:class_admins')
        )


class AssignClassAdmin(ClassroomMixin, LoginRequiredMixin, View):

    def test_func(self):
        return self.request.user.is_superuser

    def post(self, request, pk, *args, **kwargs):
        classroom_id = request.POST.get('classroom_id')
        class_admin = ClassAdmin.objects.filter(id=pk).first()
        class_admin = ClassAdmin.objects.filter(id=pk).first()
        class_admin.classroom_id = classroom_id
        class_admin.save()

        return JsonResponse({
            'redirect_url': reverse('classadmins:class_admins')
        })
