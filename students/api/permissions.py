from rest_framework.permissions import BasePermission, SAFE_METHODS

from classadmins.models import ClassAdmin


class IsSchoolAdminOrClassAdmin(BasePermission):

    def has_permission(self, request, view):
        class_admin = ClassAdmin.objects.filter(
            id=request.user.id
        ).first()
        return request.user.is_superuser or bool(class_admin)
