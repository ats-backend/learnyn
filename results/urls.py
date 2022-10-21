from django.urls import path

from results import views

app_name = 'results'

urlpatterns = [
    path('', views.ResultView.as_view(), name='result'),
    path('pdf/<int:pk>/', views.GeneratePdf.as_view(), name='pdf'),
    path('add-result/', views.AddStudentResultView.as_view(), name='add-result'),
    path('check-result/', views.CheckResultView.as_view(), name='check-result'),
    path('<int:pk>/', views.ResultDetailView.as_view(), name='result_detail'),
]
