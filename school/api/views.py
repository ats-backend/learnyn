from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView



from .serializer import (SessionSerializer, TermSerializer, 
                         SubjectSerializer, ClassroomSerializer, 
                         ClassroomDetailSerializer
                         )
from .permissions import IsSuperUser, IsSuperUserOrClassAdminOrReadOnly, IsSuperUserOrReadOnly
from school.models import Session, Term, Subject, Classroom



class ListCreateSessionAPIView(ListCreateAPIView):
    serializer_class = SessionSerializer
    queryset = Session.active_objects.all()
    permission_classes = (IsSuperUserOrReadOnly,)
    
    
class ListCreateTermAPIView(ListCreateAPIView):
    serializer_class = TermSerializer
    queryset = Term.active_objects.all()
    permission_classes = (IsSuperUserOrReadOnly,)
    
    
class ListCreateSubjectAPIView(ListCreateAPIView):
    serializer_class = SubjectSerializer
    queryset = Subject.active_objects.all()
    permission_classes = (IsSuperUserOrReadOnly, )
    
    
    
class DetailsUpdateDestroySubjectAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Subject.active_objects.all()
    serializer_class = SubjectSerializer
    permission_classes = (IsSuperUserOrReadOnly, )
    
    
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = True
        for classroom in Classroom.objects.all():
            classroom.subjects.remove(instance)
            classroom.save()
        instance.save()
        return super().delete(request, *args, **kwargs)


class ListCreateClassroomAPIView(ListCreateAPIView):
    queryset = Classroom.active_objects.all()
    serializer_class = ClassroomSerializer
    permission_classes = (IsSuperUser, )
    


class DetailsUpdateDeleteClassroomAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Classroom.active_objects.all()
    serializer_class = ClassroomDetailSerializer
    permission_classes = (IsSuperUserOrClassAdminOrReadOnly, )
    
    
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = True
        instance.save()
        return super().delete(request, *args, **kwargs)
    