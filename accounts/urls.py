from django.urls import path

from .views import LoginView, SignupView

app_name = 'accounts'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register', SignupView.as_view(), name='register'),
]
