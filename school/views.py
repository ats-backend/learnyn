from django.shortcuts import render
from django.views.generic import ListView, DetailView


from .models import Classroom

# Create your views here.




class ClassRoomListView(ListView):
    model = Classroom
    template_name = "school/classroom_list.html"
    queryset = Classroom.active_objects.all()
    context_object_name = "classrooms"

class ClassRoomDetailView(DetailView):
    model = Classroom
    template_name = "school/classroom_detail.html"
    context_object_name = "classroom"
    