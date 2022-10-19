from django.urls import path

from .views import (ClassRoomListView, ClassRoomDetailView,
                    CreateClassroomView, update_classroom,
                    DeleteRestoreClassroomView, SubjectsListView,
                    create_subject, update_subject,
                    DeleteRestoreSubjectView
                    )

app_name = "school"

urlpatterns = [

    path("", ClassRoomListView.as_view(), name="classroom_list"),
    path("details/<int:pk>", ClassRoomDetailView.as_view(), name="classroom_details"),

    path("create-classroom/", CreateClassroomView.as_view(), name="create_classroom"),
    path("update-classroom/<int:pk>/", update_classroom, name="update_classroom"),
    path("delete-classroom/<int:pk>/", DeleteRestoreClassroomView.as_view(), name="delete_restore_classroom"),

    path("subjects_list/", SubjectsListView.as_view(), name="subject_list"),
    path("create-subject/", create_subject, name="create_subject"),
    path("update-subject/<int:pk>", update_subject, name="update_subject"),
    path("delete-subject/<int:pk>", DeleteRestoreSubjectView.as_view(), name="delete_restore_subject")

]
