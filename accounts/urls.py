from django.urls import path

from .views import LoginView, LogoutView, SignupView, SetPasswordView

app_name = 'accounts'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register', SignupView.as_view(), name='register'),
    path('<int:pk>/set-password', SetPasswordView.as_view(), name='set-password')

]
