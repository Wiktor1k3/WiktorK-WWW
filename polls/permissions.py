from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # print("Checking object permission for user:", request.user)
        # print("Object owner:", obj.wlasciciel)
        # if request.method in permissions.SAFE_METHODS:
        #     return True
        return obj.wlasciciel == request.user