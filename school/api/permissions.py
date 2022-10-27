from rest_framework.permissions import BasePermission

from classadmins.models import ClassAdmin



class IsSuperUser(BasePermission):
    
    def has_permission(self, request, view):
        return bool(request.user.is_superuser)
    
    
class IsSuperUserOrReadOnly(BasePermission):
    
    def has_permission(self, request, view):
        return bool(request.user.is_superuser or request.method == "GET")
    
    
class IsSuperUserOrClassAdminOrReadOnly(BasePermission):
    
    def has_object_permission(self, request, obj, view):
        if not request.user.is_superuser:
            try:
                class_admin =  ClassAdmin.active_objects.get(id=request.user.id)
            except:
                return False
            return bool(class_admin.classroom == obj.id and request.method == "GET")
        return bool(request.user.is_superuser)