from django.urls import include, path

from .views import (
    StudentListAPIView, StudentDetailAPIView,
    SuspendStudentAPIVIew
)

app_name = 'students_api'

urlpatterns = [
    path('', StudentListAPIView.as_view(), name='api_students'),
    path('<int:pk>', StudentDetailAPIView.as_view(), name='api_student_detail'),
    path('<int:pk>/suspend', SuspendStudentAPIVIew.as_view(), name='api_suspend_student'),
]