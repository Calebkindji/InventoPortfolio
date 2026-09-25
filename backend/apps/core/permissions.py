from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit or delete it.
    Assumes model instance has a `user` attribute.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        owner = getattr(obj, 'user', None)
        if owner is None and hasattr(obj, 'portfolio'):
            owner = getattr(obj.portfolio, 'user', None)
        return owner == request.user


class IsAdminUserRole(permissions.BasePermission):
    """
    Permission check for platform administrators.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and (request.user.is_staff or request.user.role == 'ADMIN')
