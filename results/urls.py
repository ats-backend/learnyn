from django.urls import path

from results import views

app_name = 'results'

urlpatterns = [
    path('', views.ResultView.as_view(), name='result'),
    path('add-result/', views.AddStudentResultView.as_view(), name='add-result'),
    path('check-result/', views.CheckResultView.as_view(), name='check-result'),
    path('upload-result/', views.UploadResultView.as_view(), name='upload-result'),
    path('<int:pk>/', views.ResultDetailView.as_view(), name='result_detail'),
    path('pdf/<int:pk>/', views.GeneratePdf.as_view(), name='pdf'),
]
