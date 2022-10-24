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
        class_admin =  ClassAdmin.active_objects.filter(id=request.user.id).first()
        return bool(request.user.is_superuser or (class_admin.classroom == obj.id and request.method == "GET"))