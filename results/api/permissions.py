from rest_framework import permissions

from classadmins.models import ClassAdmin


class IsClassAdminOrSchoolAdmin(permissions.BasePermission):
    message = "Only class admin or school admin can add result."


    def has_object_permission(self, request, view, obj):
        class_admin = ClassAdmin.objects.get(id=request.user.id)
        # print(class_admin.classroom_id)
        # print(obj.student.classroom_id)
        return bool(request.user.is_superuser or class_admin.classroom_id == obj.student.classroom_id)
        # if request.user.is_superuser:
        #     print("Got called")
        #     return True
        # print("got called")
        # return obj.student.classroom.teacher.id == request.user.id
