from django.urls import path

from results.api.views import ResultListAPIView

app_name = 'result-api'

urlpatterns = [
    path('', ResultListAPIView.as_view(), name='result-api-view'),
]