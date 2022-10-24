from django.urls import include, path

from .views import (
    AddStudentAPIView, StudentListAPIView, StudentDetailAPIView,
    SuspendStudentAPIVIew, UploadStudentAPIView
)

app_name = 'students'

urlpatterns = [
    path('', StudentListAPIView.as_view(), name='api_students'),
    path('<int:pk>', StudentDetailAPIView.as_view(), name='api_student_detail'),
    path('<int:pk>/suspend', SuspendStudentAPIVIew.as_view(), name='api_suspend_student'),
    path('add', AddStudentAPIView.as_view(), name='api_add_student'),
    path('upload', UploadStudentAPIView.as_view(), name='api_upload_student'),
]