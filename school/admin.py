from django.contrib import admin

from .models import Classroom, Subject
# Register your models here.


class ClassRoomAdmin(admin.ModelAdmin):
    list_display = ("name", 
                    "number_of_students", 
                    "class_admin", 
                    "number_of_subjects_offerred"
                    )
    
    
# class SubjectAdmin(admin.ModelAdmin):
#     def formfield_for_manytomany(self, db_field, request, **kwargs):
#         kwargs["queryset"] = Subject.objects.filter(is_active=True)
#         return super(ClassRoomAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)
    
    
    
admin.site.register(Classroom, ClassRoomAdmin)
admin.site.register(Subject, )
