from django.urls import path

from .views import (
    AddClassAdminAPIView, AssignClassAdminAPIView, ClassAdminListAPIView,
    ClassAdminDetailAPIView, SuspendClassAdminAPIView, UnassignClassAdminAPIView
)

app_name = 'classadmins'

urlpatterns = [
    path('', ClassAdminListAPIView.as_view(), name='api_class_admins'),
    path('<int:pk>', ClassAdminDetailAPIView.as_view(), name='api_class_admin_detail'),
    path('add', AddClassAdminAPIView.as_view(), name='api_add_class_admins'),
    path('<int:pk>/toggle-suspend', SuspendClassAdminAPIView.as_view(), name='api_suspend_class_admin'),
    path('<int:pk>/unassign', UnassignClassAdminAPIView.as_view(), name='api_unassign_class_admin'),
    path('<int:pk>/assign', AssignClassAdminAPIView.as_view(), name='api_assign_class_admin'),

]
