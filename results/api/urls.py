from django.urls import path

from results.api.views import (ResultListAPIView, ResultCreateAPIView,
                               ResultDetailAPIView, CheckResultAPIView, SendResultAPIView)

app_name = 'result-api'

urlpatterns = [
    path('', ResultListAPIView.as_view(), name='result-list-api-view'),
    path('create/', ResultCreateAPIView.as_view(), name='result-create-api-view'),
    path('check-result/', CheckResultAPIView.as_view(), name='check-result'),
    path('<int:pk>/', ResultDetailAPIView.as_view(), name='result-detail-api-view'),
    path('send-result/<int:pk>/', SendResultAPIView.as_view(), name='send-result'),
]