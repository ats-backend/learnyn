from django.contrib.sites.shortcuts import get_current_site
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView

from .permissions import IsSchoolAdmin
from .serializers import ClassAdminSerializer, AssignClassroomSerializer
from ..models import ClassAdmin
from helpers.utils import send_mail


class ClassAdminListAPIView(ListCreateAPIView):
    queryset = ClassAdmin.objects.all()
    serializer_class = ClassAdminSerializer
    permission_classes = [IsSchoolAdmin]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            class_admin = serializer.save()
            subject = "Welcome to Learnyn, your new account is ready"
            password_url = reverse('accounts_api:api_set_password', args=[class_admin.id])
            action_url = str(get_current_site(self.request)) + password_url
            send_mail(
                receiver=class_admin,
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


class ClassAdminDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = ClassAdmin.objects.all()
    serializer_class = ClassAdminSerializer
    permission_classes = [IsSchoolAdmin]

    def delete(self, request, *args, **kwargs):
        class_admin = self.get_object()
        if class_admin:
            class_admin.is_deleted = True
            class_admin.save()

            return Response({
                'success': True,
                'message': "Deleted successfully"
            }, status=status.HTTP_200_OK)
        return Response({
            'success': False,
            'message': "The requested object not found"
        }, status=status.HTTP_400_BAD_REQUEST)


class SuspendClassAdminAPIView(GenericAPIView):
    queryset = ClassAdmin.objects.all()
    permission_classes = [IsSchoolAdmin]

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


class UnassignClassAdminAPIView(GenericAPIView):
    queryset = ClassAdmin.objects.all()
    permission_classes = [IsSchoolAdmin]
    serializer_class = ClassAdminSerializer

    def put(self, request, *args, **kwargs):
        try:
            class_admin = self.get_object()
            class_admin.classroom = None
            class_admin.save()
            serializer = ClassAdminSerializer(class_admin)
            return Response({
                'success': True,
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        except:
            return Response({
                'success': False,
                'error': "No such class admin exist"
            }, status=status.HTTP_400_BAD_REQUEST)


class AssignClassAdminAPIView(GenericAPIView):
    queryset = ClassAdmin.objects.all()
    permission_classes = [IsSchoolAdmin]
    serializer_class = ClassAdminSerializer

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = ClassAdminSerializer(
            instance,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            'success': False,
            'error': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

