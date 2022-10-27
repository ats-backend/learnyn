from datetime import timedelta
from random import randint

from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

from rest_framework_simplejwt.views import TokenObtainPairView

from classadmins.models import ClassAdmin
from helpers.utils import send_password_reset_mail
from .serializers import (
    LoginSerializer, RegisterAdminSerializer, SetPasswordSerializer,
    ResetPasswordSerializer, ResetPasswordTokenSerializer
)
from .token import get_token

from ..models import ResetPasswordToken


class LoginAPIView(TokenObtainPairView):
    serializer_class = LoginSerializer


class LogoutAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        token = request.META.get('HTTP_AUTHORIZATION').split(" ")[1]
        access = AccessToken(token)
        refresh = RefreshToken.for_user(request.user)
        access.set_exp(lifetime=timedelta(days=0))
        refresh.lifetime = timedelta(days=0)
        logout(request)

        return Response({
            'success': True,
            'message': "User successfully logged out"
        })


class SignupAPIView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = RegisterAdminSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = get_token(user)
            return Response(
                {
                    'success': True,
                    'data': serializer.data,
                    'tokens': token
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
        uid = urlsafe_base64_decode(kwargs['uid'])
        serializer = SetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.filter(id=uid).first()
            user.set_password(serializer.data['password'])
            user.save()
            return Response({
                'success': True,
                'message': "Password set successfully"
            })

        return Response({
            'success': False,
            'data': serializer.errors
        })


class ResetPasswordAPIView(GenericAPIView):

    def post(self, request, *args, **kwargs):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.data['email']
            user = User.objects.get(email=email)
            try:
                reset_password = ResetPasswordToken.objects.get(user=user)
            except:
                reset_password = ResetPasswordToken.objects.create(
                    user=user,
                    token=randint(99, 9999),
                )

            context = {
                "user": user,
                "token": reset_password.token
            }

            email_body = {
                "subject": "Password Reset From Learnyn",
                "recipient": email,
            }

            send_password_reset_mail(email_body, context)
            return Response({
                'success': True,
                'token': reset_password.token,
                'validate_token_url': reverse('accounts_api:api_validate_password_token')
            })
        return Response({
            'success': False,
            'error': serializer.errors
        })


class ValidateRestPasswordTokenAPIView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = ResetPasswordTokenSerializer(data=request.data)
        if serializer.is_valid():
            token = serializer.data['token']
            reset_token = ResetPasswordToken.objects.get(token=token)
            uid = urlsafe_base64_encode(force_bytes(reset_token.user_id))

            return Response({
                'success': True,
                'set_password_url': reverse("accounts_api:api_set_password", args=[uid])
            })

        return Response({
            'success': False,
            'error': serializer.errors
        })
