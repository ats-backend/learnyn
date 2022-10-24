from django.urls import path

from .views import (
    LoginAPIView, LogoutAPIView,
    SetPasswordAPIView, SignupAPIView
)

app_name = 'accounts'

urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='api_login'),
    path('logout/', LogoutAPIView.as_view(), name='api_logout'),
    path('register', SignupAPIView.as_view(), name='api_register'),
    path('<int:pk>/set-password', SetPasswordAPIView.as_view(), name='api_set_password'),

    # path("reset-password/", ResetPasswordView.as_view(), name='reset_password'),
    # path("validate-password-token/", validate_reset_password_token, name="validate_password_token"),
    # path("<str:uid>/new-password/", new_password, name="new_password"),
]
