from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView, View
from django.contrib import messages
from django.db.models import Q


from .models import Classroom, Subject
from .forms import ClassroomForm, SubjectForm
from accounts.models import Student

# Create your views here.


class ClassRoomListView(ListView):
    model = Classroom
    template_name = "school/classroom_list.html"
    # queryset = Classroom.active_objects.all()
    # context_object_name = "classrooms"
    
    def get_context_data(self, **kwargs) :
        search = self.request.GET.get("classroom") if self.request.GET.get("classroom") is not None else "" 
        context = super(ClassRoomListView, self).get_context_data(**kwargs)
        context["classrooms"] =  Classroom.active_objects.filter(Q(name__icontains=search) | Q(category__icontains=search) 
                                                                 | Q(description__icontains=search))
        return context

class ClassRoomDetailView(DetailView):
    model = Classroom
    template_name = "school/classroom_detail.html"
    
    def get_context_data(self, **kwargs):
        context = super(ClassRoomDetailView, self).get_context_data(**kwargs)
        context["classroom"] = Classroom.active_objects.get(id=self.kwargs["pk"])
        context["students"] = Student.objects.filter(classroom_id=self.kwargs["pk"])
        return context
    


def create_subject(request):
    
    if request.method == "POST":
        form = ClassroomForm(request.POST)
        
        if form.is_valid():
            form.save()
            
            messages.success(request, "Subject created successfully")
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
        
        errors = (form.errors.as_text()).split("*")
        messages.error(request, errors[len(errors) - 1])
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    
    return


def update_subject(request, pk):
    try:
        subject = Subject.active_objects.get(id=pk)
    except Subject.DoesNotExist:
        messages.error(request, "Subject Does Not Exist !")
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
        
    
    if request.method == "GET":
        form = SubjectForm(request.POST, instance=subject)
        
        if form.is_valid():
            form.save()
            
            messages.success(request, f"{subject.name} updated successfully")
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
        
        errors = (form.errors.as_text()).split("*")
        messages.error(request, errors[len(errors) - 1])
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    return



class DeleteRestoreSubjectView(View):
    def get(self, request, **kwargs):
        try:
            instance = Subject.objects.get(id=kwargs["pk"])
        except Subject.DoesNotExist:
            messages.error(request, "Subject Does Not Exist !")
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
        
        instance.is_active = not instance.is_active
        instance.save()
        
        if not instance.is_active:
            messages.success(request, f"{instance.name} deleted successfully !")
        else:
            messages.error(request, f"{instance.name} restored successfully !")
            
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    

class CreateClassroomView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "school/create_classroom.html", {"form": ClassroomForm()})
    
    def post(self, request, *args, **kwargs):
        form = ClassroomForm(request.POST, request.FILES)
        
        if form.is_valid():
            form.save()
            
            messages.success(request, f"{request.POST['name']} Created Successfully !")
            return HttpResponseRedirect(reverse("school:create_classroom"))
        errors = (form.errors.as_text()).split("*")
        messages.error(request, errors[len(errors) - 1 ])
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    

def update_classroom(request, pk):
    try:
        classroom = Classroom.active_objects.get(id=pk)
    except Classroom.DoesNotExist:
        messages.error(request, "Classroom Does Not Exist !")
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    
    if request.method == "POST":
        form = ClassroomForm(request.POST, instance=classroom)
        
        if form.is_valid():
            form.save()
             
            messages.success(request, f"{classroom.name} updated successfully")
            return HttpResponseRedirect(reverse("school:classroom_details", args=[pk]))
        errors = (form.errors.as_text()).split("*")
        messages.error(request, errors[len(errors) - 1 ])
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    return render(request, "school/create_classroom.html", {"form": ClassroomForm(instance=classroom), "instance": classroom })
    

class DeleteRestoreClassroomView(View):
    def get(self, request, **kwargs):
        try:
            instance = Classroom.objects.get(id=kwargs["pk"])
        except Classroom.DoesNotExist:
            messages.error(request, "Classroom Does Not exist")
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
        
        instance.is_active = not instance.is_active 
        instance.save()
        
        if not instance.is_active:
            messages.error(request, f"{instance.name} deleted successfully !")
        else:
            messages.error(request, f"{instance.name} restored successfully !")
        return HttpResponseRedirect(reverse("school:classroom_list"))



class SubjectsListView(ListView):
    model = Subject
    template_name = "school/subjects_dashboard.html"
    queryset = Subject.active_objects.all()
    context_object_name = "subjects"