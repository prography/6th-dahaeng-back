from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response

from config.permissions import MyIsAuthenticated
from core.models import Jorang, UserCoin, Profile
from core.ERROR.error_cases import GlobalErrorMessage
from record.models import Post


# profile/<int:profile_id>/
class ProfileDetailView(APIView):
    permission_classes = [MyIsAuthenticated, ]

    def get_object(self, profile_id):
        try:
            return Profile.objects.get(id=profile_id)
        except Profile.DoesNotExist:
            raise Http404

    def get(self, request, profile_id):
        """
        profile_id 에 해당하는 profile 객체에 대하여,
        profile, user_coin, user_continuity, jorang 에 관한 정보들을 넘겨준다.

        TODO: orm 개선
        TODO: permission denined 를 custom 해서 할 수 있게 해야한다.
        """
        # 본인의 정보만 가져와야 한다.
        if int(request.user.pk) != int(profile_id):
            raise GlobalErrorMessage('본인의 정보를 들고 오는 것이 아닙니다.')

        profile = self.get_object(profile_id)

        try:
            jorang = Jorang.objects.get(profile=profile.id)
        except Jorang.DoesNotExist:
            raise GlobalErrorMessage('해당 유저는 조랭이를 만들지 않았습니다. 조랭이를 만들어 주세요.')

        user_coin = UserCoin.objects.get(profile=profile.id)

        try:
            post = Post.objects.get(
                profile=profile.id, created_at=user_coin.last_date)
            continuity = post.continuity
        except Post.DoesNotExist:
            continuity = 0

        return Response({
            'response': 'success',
            'message': {
                'email': profile.email,
                'title': jorang.title,
                'jorang_nickname': jorang.nickname,
                'jorang_color': jorang.color,
                'jorang_status': jorang.status,
                'user_continuity': continuity,
                'user_coin': user_coin.coin
            }
        })

    def post(self, request, profile_id):
        """
        조랭이의 상세 정보, nickname 과 title 을 input 으로 받아
        그것을 저장하고, 그 값을 돌려보내준다.
        """
        # 본인의 정보만 가져와야 한다.
        if int(request.user.pk) != int(profile_id):
            raise GlobalErrorMessage('본인의 정보를 들고 오는 것이 아닙니다.')

        profile = self.get_object(profile_id)
        user_coin = UserCoin.objects.get(profile=profile.id)

        try:
            post = Post.objects.get(
                profile=profile.id, created_at=user_coin.last_date)
            continuity = post.continuity
        except Post.DoesNotExist:
            continuity = 0

        nickname = request.data.get('nickname')
        title = request.data.get('title')

        try:
            jorang = Jorang.objects.get(profile=profile.id)
        except Jorang.DoesNotExist:
            raise GlobalErrorMessage('해당 유저는 조랭이를 만들지 않았습니다. 조랭이를 만들어 주세요.')

        jorang.nickname = nickname
        jorang.title = title
        jorang.save()

        return Response({
            'response': 'success',
            'message': {
                'email': profile.email,
                'title': jorang.title,
                'jorang_nickname': jorang.nickname,
                'jorang_color': jorang.color,
                'jorang_status': jorang.status,
                'user_continuity': continuity,
                'user_coin': user_coin.coin
            }
        })
