from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminUserOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        """
        Allows only administrators to create, modify, or delete.
        Other users can only read.
        """
        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user.is_staff
