from django.contrib.auth import get_user_model
from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response

from core.models import Jorang, UserCoin


# profile/<int:profile_id>/
class ProfileDetailView(APIView):
    def get_object(self, profile_id):
        try:
            return get_user_model().objects.get(id=profile_id)
        except get_user_model().DoesNotExist:
            raise Http404

    def get(self, request, profile_id):
        """
        profile_id 에 해당하는 Profile 과 그의 조랭이 의 정보를 넘겨준다.

        TODO: orm 개선
        그런데, jorang 과 usercoin 모두 1:1 인데, 크게 시간적으로 문제가 될 수 있을까?

        :param request:
        :param profile_id: profile/<int:profile_id>/
        :return:
        """

        profile = self.get_object(profile_id)
        jorang = Jorang.objects.get(profile=profile.id)
        usercoin = UserCoin.objects.get(profile=profile.id)

        # TODO: record.Post 구현 이후, 이부분을 수정한다.
        """
        try:
            post = Post.objects.get(
                profile=profile.id, created_at=usercoin.last_date)
            continuity = post.continuity
        except Post.DoesNotExist:
            continuity = 0
        """

        return Response({
            'response': 'success',
            'message': {
                'email': profile.email,
                'title': jorang.title,
                'jorang_nickname': jorang.nickname,
                'jorang_color': jorang.color,
                'jorang_status': jorang.status,
                'user_continuity': 0,  # TODO: record 구현 이후, 이부분을 수정한다.
                'user_coin': usercoin.coin
            }
        })

    def post(self, request, profile_id):
        """
        조랭이의 상세 정보, nickname 과 title 을 input 으로 받아
        그것을 저장하고, 그 값을 돌려보내준다.

        :param request:
        :param profile_id:
        :return:
        """
        profile = self.get_object(profile_id)
        usercoin = UserCoin.objects.get(profile=profile.id)

        # TODO: record.Post 구현 이후, 이부분을 수정한다.
        """
        try:
            post = Post.objects.get(
                profile=profile.id, created_at=usercoin.last_date)
            continuity = post.continuity
        except Post.DoesNotExist:
            continuity = 0
        """

        nickname = request.data.get('nickname')
        title = request.data.get('title')

        jorang = Jorang.objects.get(profile=profile.id)
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
                'user_continuity': 0,  # TODO: record 구현 이후, 이부분을 수정한다.
                'user_coin': usercoin.coin
            }
        })
