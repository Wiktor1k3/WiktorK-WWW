from rest_framework import permissions
import copy

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # print("Checking object permission for user:", request.user)
        # print("Object owner:", obj.wlasciciel)
        # if request.method in permissions.SAFE_METHODS:
        #     return True
        return obj.wlasciciel == request.user

class CustomDjangoModelPermissions(permissions.DjangoModelPermissions):

    def __init__(self):
        self.perms_map = copy.deepcopy(self.perms_map)
        self.perms_map['GET'] = ['%(app_label)s.view_%(model_name)s']
