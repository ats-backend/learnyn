from rest_framework.serializers import ModelSerializer, HyperlinkedIdentityField

from school.models import Session, Term, Subject, Classroom


class SessionSerializer(ModelSerializer):
    class Meta:
        model = Session
        fields = ("name_of_session", )
        
        
class TermSerializer(ModelSerializer):
    class Meta:
        model = Term
        fields = ("session", "term")
   
        
class SubjectSerializer(ModelSerializer):
    class Meta:
        model = Subject
        fields = ("name", )
        

class ClassroomSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(view_name="school_api:classroom_details_update_delete", read_only=True)
    subjects = SubjectSerializer(many=True)
    class Meta:
        model = Classroom
        fields = ("name", "category", "subjects", "description", 'url')
        
        
class ClassroomDetailSerializer(ModelSerializer):
    subjects = SubjectSerializer(many=True)
    class Meta:
        model = Classroom
        fields = ("name", "category", "subjects", "description")