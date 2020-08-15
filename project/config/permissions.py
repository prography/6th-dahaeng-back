from rest_framework import permissions

# TODO: 이것도 써야하나?
# class IsEmailAuthenticated(permissions.BasePermission):
#     def has_permissions(self, request, view):
#         return request.user.status != '0'


class MyIsAuthenticated(permissions.BasePermission):
    """
        아직 확실하게 확인을 하지는 못하였으나,
        이과정을 통해서 미리 JWT toekn 을 통해서
        request.user 에 user 를 미리 집어 넣어둔것으로 확인을 할 수 있었다.

    """
    message = ''

    def has_permission(self, request, view):
        # AnonymousUser 가 나올 경우도 있는데, 즉 확인 되지 않은 USER 라는 의미이다.
        print("MyIsAuthenticated request", request)
        print("request.user", request.user)
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


