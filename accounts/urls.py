from django.urls import path

from .views import (LoginView, LogoutView,
                    SignupView, SetPasswordView,
                    ResetPasswordView, validate_reset_password_token, new_password
                    )

app_name = 'accounts'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register', SignupView.as_view(), name='register'),
    path('<int:pk>/set-password', SetPasswordView.as_view(), name='set-password'),

    path("reset-password/", ResetPasswordView.as_view(), name='reset_password'),
    path("validate-password-token/", validate_reset_password_token, name="validate_password_token"),
    path("<str:uid>/new-password/", new_password, name="new_password"),

]

# urlpatterns += [
#     path('api'/)
# ]