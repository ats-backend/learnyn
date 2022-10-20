"""learnyn URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from accounts.views import (
    AddClassAdminView, AddStudentView, AssignClassAdmin, DashboardView,
    ClassAdminListView, ClassAdminDetailView, StudentListView,
    StudentDetailView, SuspendClassAdmin, UnassignClassAdmin
)

from .views import detail, profile, item_list, item_list_two, results

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('class-admins', ClassAdminListView.as_view(), name='class_admins'),
    path('class-admins/<int:pk>', ClassAdminDetailView.as_view(), name='class_admin_detail'),
    path('class-admins/add', AddClassAdminView.as_view(), name='add_class_admins'),
    path('class-admins/<int:pk>/toggle-suspend', SuspendClassAdmin.as_view(), name='suspend_class_admin'),
    path('class-admins/<int:pk>/unassign', UnassignClassAdmin.as_view(), name='unassign_class_admin'),
    path('class-admins/<int:pk>/assign', AssignClassAdmin.as_view(), name='assign_class_admin'),
    path('students', StudentListView.as_view(), name='students'),
    path('students/<int:pk>', StudentDetailView.as_view(), name='student_detail'),
    path('students/add', AddStudentView.as_view(), name='add_student'),

    path('profile', profile, name='profile'),
    path('list', item_list, name='list'),
    path('list-two', item_list_two, name='list-two'),
    path('detail', detail, name='detail'),
    path('results', results, name='results'),
    path('accounts/', include('accounts.urls')),
    path('admin/', admin.site.urls),
    path("school/", include("school.urls"))

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
