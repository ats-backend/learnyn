from django.urls import path


from .views import(ListCreateSessionAPIView, ListCreateTermAPIView, 
                   ListCreateSubjectAPIView, DetailsUpdateDestroySubjectAPIView, 
                   ListCreateClassroomAPIView, DetailsUpdateDeleteClassroomAPIView
                   )


app_name = "school_api"


urlpatterns = [
    path("session-list-create/", ListCreateSessionAPIView.as_view(), name="session_list_create"),
    
    path("term-list-create/", ListCreateTermAPIView.as_view(), name="term_list_create"), 
    
    path("subject-list-create/", ListCreateSubjectAPIView.as_view(), name="subject_list_create"),
    path("subject-detail-update-delete/<int:pk>/", DetailsUpdateDestroySubjectAPIView.as_view(), name="term_detail_update_delete"),
    
    path("classroom-list-create/", ListCreateClassroomAPIView.as_view(), name="classroom_list_create"),
    path("classroom-details-update-delete/<int:pk>/", DetailsUpdateDeleteClassroomAPIView.as_view(), name="classroom_details_update_delete")
    
    
]
