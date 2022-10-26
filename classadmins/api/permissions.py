from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsSchoolAdmin(BasePermission):

    def has_permission(self, request, view):

        return request.user.is_superuser
