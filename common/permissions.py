from rest_framework.permissions import BasePermission

SAFE_METHODS = ("GET", "HEAD", "OPTIONS")


class IsAdminOrAuthenticatedReadOnly(BasePermission):
    """
    Allow CRUD to staff/admin users
    Allow Read only to non-admin users
    """

    def has_permission(self, request, view):
        return bool(
            request.user.is_authenticated
            and request.method in SAFE_METHODS
            or request.user.is_staff
            and request.user.is_authenticated
        )
