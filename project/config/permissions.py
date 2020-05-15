from rest_framework import permissions

# TODO: 이것도 써야하나?
# class IsEmailAuthenticated(permissions.BasePermission):
#     def has_permissions(self, request, view):
#         return request.user.status != '0'


class MyIsAuthenticated(permissions.BasePermission):
    message = 'Adding customers not allowed.'

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.status == '1')
