from rest_framework import permissions


class IsHe(permissions.BasePermission):

    def has_permission(self, request, view):
        """ Si el kword que es el id del user para filtrar, no coincide 
        con el user que esta logueando, lo rechazo """
        user = request.query_params.get('user','')
        user_loggin = request.user.id
        user = int(user)
        user_loggin = int(user)

        if user == user_loggin:
            return True
        else:
            return False

class isHeRetrive(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        if obj.user == request.user:
            return True
        else:
            return False

        