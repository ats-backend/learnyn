from django.contrib import admin

from .models import Classroom, Subject
# Register your models here.


class ClassRoomAdmin(admin.ModelAdmin):
    list_display = ("name", "number_of_students", "class_admin", "number_of_subjects_offerred")
    
    
    
admin.site.register(Classroom, ClassRoomAdmin)
admin.site.register(Subject)
