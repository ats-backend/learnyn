from rest_framework.views import APIView

from students.forms import StudentForm
from accounts.views import ClassroomMixin
from classadmins.models import ClassAdmin
from students.models import Student
from helpers.utils import send_mail, send_password_reset_mail
from school.models import Classroom

# Create your views here.


class AddStudentAPIView(APIView):
    pass


class StudentListAPIView(APIView):
    pass


class StudentDetailAPIView(APIView):
    pass


class UploadStudentAPIView(APIView):
    pass


class SuspendStudentAPIVIew(APIView):
    pass

