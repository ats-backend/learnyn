from django.urls import path

from .views import ClassRoomListView, ClassRoomDetailView



app_name = "school"


urlpatterns = [
    path("", ClassRoomListView.as_view(), name="classroom_list"),
    path("details/<int:pk>", ClassRoomDetailView.as_view(), name="classroom_details" )
]