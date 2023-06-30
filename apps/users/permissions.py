from rest_framework import permissions


class IsHe(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if obj == request.user:
            return True
        else:
            return False

