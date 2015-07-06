from rest_framework import permissions

from vacation_app.models import Employee

class IsAdminEmployee(permissions.BasePermission):
    """
    Is admin in vacation_app
    """
    def has_permission(self, request, view):
        user = False
        if hasattr(request.user, 'group_code'):
            if request.user.group_code == Employee.GADMIN:
                user = True
        return user


class IsAuthenticatedOrCreateOnly(permissions.BasePermission):
    """
    The request is authenticated as a user, or is a create-only request.
    """

    def has_permission(self, request, view):
        return (
            request.method == 'POST' or
            request.user and
            request.user.is_authenticated()
        )