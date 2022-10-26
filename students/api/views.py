from django.contrib.sites.shortcuts import get_current_site
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from classadmins.models import ClassAdmin
from helpers.utils import send_mail
from ..models import Student
from .permissions import IsSchoolAdminOrClassAdmin
from .serializers import StudentSerializer


class StudentListAPIView(ListCreateAPIView):
    queryset = Student.objects.all()
    permission_classes = [IsSchoolAdminOrClassAdmin]
    serializer_class = StudentSerializer

    def get_queryset(self):
        if ClassAdmin.active_objects.filter(
                id=self.request.user.id
        ).exists():
            class_admin = ClassAdmin.active_objects.filter(
                id=self.request.user.id
            ).first()
            return class_admin.classroom.students.all()
        return self.queryset

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            student = serializer.save()
            subject = "Welcome to Learnyn, your new student account is ready"
            from rest_framework.reverse import reverse
            password_url = reverse('accounts_api:api_set_password', args=[student.id])
            action_url = str(get_current_site(self.request)) + password_url
            send_mail(
                receiver=student,
                subject=subject,
                action_url=action_url
            )
            return Response(
                {
                    'success': True,
                    'data': serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {
                'success': False,
                'data': serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )


class StudentDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Student.active_objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsSchoolAdminOrClassAdmin]

    def delete(self, request, *args, **kwargs):
        student = self.get_object()
        if student:
            student.is_deleted = True
            student.save()

            return Response({
                'success': True,
                'message': "Deleted successfully"
            }, status=status.HTTP_200_OK)
        return Response({
            'success': False,
            'message': "The requested object not found"
        }, status=status.HTTP_400_BAD_REQUEST)


class SuspendStudentAPIVIew(GenericAPIView):
    queryset = Student.active_objects.all()
    permission_classes = [IsSchoolAdminOrClassAdmin]

    def put(self, request, *args, **kwargs):
        try:
            class_admin = self.get_object()
            class_admin.is_suspended = not class_admin.is_suspended
            class_admin.save()
            return Response({
                'success': True,
                'suspended': class_admin.is_suspended
            }, status=status.HTTP_200_OK)
        except:
            return Response({
                'success': False,
                'error': "No such class admin exist"
            }, status=status.HTTP_400_BAD_REQUEST)
