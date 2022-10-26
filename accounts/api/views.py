from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from classadmins.models import ClassAdmin
from .serializers import LoginSerializer, RegisterAdminSerializer, SetPasswordSerializer


class LoginAPIView(TokenObtainPairView):
    serializer_class = LoginSerializer


class TokenRefreshAPIView(TokenRefreshView):
    pass


class LogoutAPIView(APIView):
    pass


class SignupAPIView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = RegisterAdminSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
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


class SetPasswordAPIView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = SetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            class_admin = ClassAdmin.objects.filter(id=kwargs['pk']).first()
            class_admin.set_password(serializer.data['password'])
            class_admin.save()
            print(class_admin, serializer.data)
            return Response({
                'success': True,
                'message': "Password set successfully"
            })

        return Response({
            'success': False,
            'data': serializer.errors
        })
