from rest_framework import permissions


class IsAuthenticatedReadOnly(permissions.BasePermission):
    """
    The request is authenticated as a user, but it does not have permissions
    to change the resource.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return False


class IsAdminOrSelf(permissions.BasePermission):
    """
    Only admin or owner can edit.
    """

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        return obj == request.user


class IsAuthorIpr(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            or request.user.is_staff
        )
    
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class IsAuthorIprOrIsEmployee(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            or request.user.is_staff
        )
    
    def has_object_permission(self, request, view, obj):
        return (
            obj.author == request.user
            or (
                obj.employee == request.user
                and request.method in ['PUT', 'PATCH']
            )
        )