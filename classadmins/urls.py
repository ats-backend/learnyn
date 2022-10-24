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

from classadmins.views import (
    AddClassAdminView, AssignClassAdmin, ClassAdminListView,
    ClassAdminDetailView, SuspendClassAdmin, UnassignClassAdmin
)

app_name = 'classadmins'

urlpatterns = [
    path('', ClassAdminListView.as_view(), name='class_admins'),
    path('<int:pk>', ClassAdminDetailView.as_view(), name='class_admin_detail'),
    path('add', AddClassAdminView.as_view(), name='add_class_admins'),
    path('<int:pk>/toggle-suspend', SuspendClassAdmin.as_view(), name='suspend_class_admin'),
    path('<int:pk>/unassign', UnassignClassAdmin.as_view(), name='unassign_class_admin'),
    path('<int:pk>/assign', AssignClassAdmin.as_view(), name='assign_class_admin'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
