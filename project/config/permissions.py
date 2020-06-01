from rest_framework import permissions

# TODO: 이것도 써야하나?
# class IsEmailAuthenticated(permissions.BasePermission):
#     def has_permissions(self, request, view):
#         return request.user.status != '0'


class MyIsAuthenticated(permissions.BasePermission):
    message = ''

    def has_permission(self, request, view):
        if request.user.is_anonymous:
            self.message = '유저가 존재하지 않습니다.'
            return False

        elif bool(request.user.status == '0'):
            self.message = '이메일 인증이 필요합니다.'
            return False

        elif not bool(request.user.is_authenticated):
            self.message = '로그인이 필요합니다.'
            return False

        return True

        # message 변경을 위해 변경
        # return bool(request.user and request.user.is_authenticated and request.user.status == '1')
