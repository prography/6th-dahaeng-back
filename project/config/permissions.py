from rest_framework.permissions import BasePermission
from core.ERROR.error_cases import GlobalErrorMessage401


class MyIsAuthenticated(BasePermission):
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


class IsOwnedByProfile(BasePermission):
    def has_object_permission(self, request, view, obj):
        if not (obj.profile.pk == request.user.pk):
            raise GlobalErrorMessage401(str("다른 사람의 일기는 볼 수 없어요."))
        return True