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
    AddClassAdminView, AddStudentView, AssignClassAdmin,
    ClassAdminListView, ClassAdminDetailView, DownloadStudentDataView,
    HomeView, StudentListView, StudentDetailView, SuspendClassAdmin,
    SuspendStudent, UnassignClassAdmin, UploadStudentView
)

from .views import detail, profile, item_list, item_list_two, results

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('class-admins', ClassAdminListView.as_view(), name='class_admins'),
    path('class-admins/<int:pk>', ClassAdminDetailView.as_view(), name='class_admin_detail'),
    path('class-admins/add', AddClassAdminView.as_view(), name='add_class_admins'),
    path('class-admins/<int:pk>/toggle-suspend', SuspendClassAdmin.as_view(), name='suspend_class_admin'),
    path('class-admins/<int:pk>/unassign', UnassignClassAdmin.as_view(), name='unassign_class_admin'),
    path('class-admins/<int:pk>/assign', AssignClassAdmin.as_view(), name='assign_class_admin'),
    path('students', StudentListView.as_view(), name='students'),
    path('students/<int:pk>', StudentDetailView.as_view(), name='student_detail'),
    path('students/<int:pk>/suspend', SuspendStudent.as_view(), name='suspend_student'),
    path('students/add', AddStudentView.as_view(), name='add_student'),
    path('students/upload', UploadStudentView.as_view(), name='upload_student'),
    path('classroom/<int:pk>/students/download', DownloadStudentDataView.as_view(), name='download_student_data'),

    path('profile', profile, name='profile'),
    path('list', item_list, name='list'),
    path('list-two', item_list_two, name='list-two'),
    path('detail', detail, name='detail'),
    path('accounts/', include('accounts.urls')),
    path('results/', include('results.urls')),
    path('admin/', admin.site.urls),
    path("school/", include("school.urls"))

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
