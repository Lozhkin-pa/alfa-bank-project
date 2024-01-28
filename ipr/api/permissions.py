from rest_framework import permissions


class IsAuthenticatedReadOnly(permissions.BasePermission):
    """
    The request is authenticated as a user, but it does not have permissions
    to change the resource.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return False


class IsAdminOrSelf(permissions.BasePermission):
    """
    Only admin or owner can edit.
    """

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        return obj == request.user
