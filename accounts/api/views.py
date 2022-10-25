from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .serializers import LoginSerializer, RegisterAdminSerializer


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
    pass