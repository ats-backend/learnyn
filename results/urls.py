from django.urls import path

from results import views

app_name = 'results'

urlpatterns = [
    path('result/<int:pk>/', views.ResultView.as_view(), name='result'),
    path('pdf/', views.GeneratePdf.as_view(), name='pdf')
]
