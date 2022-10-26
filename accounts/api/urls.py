from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    LoginAPIView, LogoutAPIView, ResetPasswordAPIView,
    SetPasswordAPIView, SignupAPIView,
    ValidateRestPasswordTokenAPIView
)

app_name = 'accounts_api'

urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='api_login'),
    path('login-api-refresh/', TokenRefreshView.as_view(), name='api_refresh'),
    path('logout/', LogoutAPIView.as_view(), name='api_logout'),
    path('register', SignupAPIView.as_view(), name='api_register'),
    path('<str:uid>/set-password', SetPasswordAPIView.as_view(), name='api_set_password'),
    path("reset-password/", ResetPasswordAPIView.as_view(), name='api_reset_password'),
    path("validate-password-token/",
         ValidateRestPasswordTokenAPIView.as_view(),
         name="api_validate_password_token"
         ),
]
