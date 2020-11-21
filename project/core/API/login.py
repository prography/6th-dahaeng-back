# Swagger
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

# third
from datetime import date

# Django
from django.contrib.auth.models import update_last_login
from django.http import HttpResponseRedirect
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
# DRF
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework_jwt.views import ObtainJSONWebToken

# custom
from config.permissions import MyIsAuthenticated
from core.models import Jorang, Profile, UserCoin
from core.serializers import ProfileSerializer
from core.API.email import send_email_for_active
from core.API.jorang import downgrade_jorang_status
from core.API.util import get_id_of_today_post
from core.API.request_format_serializers import LoginSerializer
from core.ERROR.error_cases import GlobalErrorMessage
from record.serializers import UserQuestionSerializer
from record.models import UserQuestion


# /sighup/ 회원 가입
class CreateProfileView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        """
            신규 사용자의 email 과 password 를 받아.
            새로운 Profile 을 만들어준다.
            {
                "profile": {
                    "email": "rkdalstjd9@naver.com",
                    "password": "qwe123"
                }
            }
            email 전송 성공 -> 잘 되었다고 응답.
            email 전송 실패 -> 만든 profile 삭제.
        """

        data = request.data.get('profile')
        if not data:
            raise GlobalErrorMessage("profile 파라미터가 없습니다.")

        profile_serializer = ProfileSerializer(data=data)
        if profile_serializer.is_valid():
            profile = profile_serializer.save()
        else:
            raise GlobalErrorMessage(str(profile_serializer.errors))

        email_result = send_email_for_active(profile, request)

        if email_result:
            return Response({
                'response': 'success',
                'message': '이메일을 전송하였습니다.'
            })
        profile.delete()
        raise GlobalErrorMessage("이메일을 전송에 실패하였습니다.")


# /user_active/
class UserActivateView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        print("request.query_params", request.query_params)
        profile_id = request.query_params["profile_id"]
        token = request.query_params["token"]
        print("profile_id", profile_id, "token", token)
        if profile_id is None or token is None:
            # raise GlobalErrorMessage("profile_id64 or token 이 존재하지 않습니다.")
            return HttpResponseRedirect(redirect_to='https://da-haeng-b4f92.web.app')
        if profile_id[-1] == "/":
            profile_id = profile_id[:-1]
        if token[-1] == "/":
            token = token[:-1]

        print("profile_id", profile_id, "token", token)

        try:
            profile = Profile.objects.get(id=int(profile_id))
        except Profile.DoesNotExist:
            # raise GlobalErrorMessage(f' profile pk= {profile_id}에 해당하는 유저가 없습니다.')
            return HttpResponseRedirect(redirect_to='https://da-haeng-b4f92.web.app')

        if profile.email_token.token == token:
            profile.status = '1'
            profile.save()
        else:
            # raise GlobalErrorMessage('유효하지 않은 token 입니다.')
            return HttpResponseRedirect(redirect_to='https://da-haeng-b4f92.web.app')
        return HttpResponseRedirect(redirect_to='https://da-haeng-b4f92.web.app')

    def post(self, request):
        """
                Email 로 보낸 것에 대해서,
                {
                    'profile_id64': profile_id64,
                    'token': token
                }
                을 받아, profile_id64 -> Profile 객체를 이끌어 오고,
                token 을 다시 profile 객체로 만들어 비교를 한다.
                올바르다면, user 를 activate 시켜준다.
            """

        profile_id = request.data.get('profile_id')
        token = request.data.get('token')
        # print("profile_id", profile_id, "token", token)

        if profile_id is None or token is None:
            # raise GlobalErrorMessage("profile_id64 or token 이 존재하지 않습니다.")
            return HttpResponseRedirect(redirect_to='https://da-haeng-b4f92.web.app')

        try:
            profile = Profile.objects.get(id=int(profile_id))
        except Profile.DoesNotExist:
            # raise GlobalErrorMessage(f' profile pk= {profile_id}에 해당하는 유저가 없습니다.')
            return HttpResponseRedirect(redirect_to='https://da-haeng-b4f92.web.app')

        if profile.email_token.token == token:
            profile.status = '1'
            profile.save()
        else:
            # raise GlobalErrorMessage('유효하지 않은 token 입니다.')
            return HttpResponseRedirect(redirect_to='https://da-haeng-b4f92.web.app')
        return HttpResponseRedirect(redirect_to='https://da-haeng-b4f92.web.app')


@extend_schema(
    responses=LoginSerializer,
    auth=None,
    tags=["A - New - Core - Login"],
    summary="POST Login"
)
# /login/
class MyObtainJSONWebToken(ObtainJSONWebToken):
    def post(self, request):
        """
            today_post_id : 오늘 작성한 포스트 id 반환
                * 오늘 작성한 일기가 있는 경우 : 해당 id
                * 오늘 작성한 일기가 없는 경우 : -1
        """
        # 계정 활성화 check
        email = request.data.get('email', '')
        try:
            profile = Profile.objects.get(email=email)
            if not profile.is_active:
                raise GlobalErrorMessage(
                    '활성화 되지 않은 계정입니다. 메일을 확인하고, 본인인증을 해주세요.')
        except Profile.DoesNotExist:
            raise GlobalErrorMessage('유효하지않은 계정입니다.')

        # jwt token get
        response = super().post(request, content_type='application/json')
        if response.status_code != 200:
            raise GlobalErrorMessage('JWT token 생성에 실패하였습니다.')

        # 처음 로그인일 경우
        if profile.last_login is None:
            UserQuestion.objects.create(profile=profile)
            UserCoin.objects.create(profile=profile)
        if str(profile.last_login).split()[0] < str(date.today()):
            downgrade_jorang_status(profile)

        # 조랭이 check
        try:
            jorang = Jorang.objects.get(profile=profile)
            has_jorang = True
            jorang_nickname = jorang.nickname
            jorang_color = jorang.color
        except Jorang.DoesNotExist:
            has_jorang = False
            jorang_nickname = None
            jorang_color = None

        update_last_login(None, profile)
        today_post_id = get_id_of_today_post(profile)

        return Response({
            'response': 'success',
            'message': {
                'token': response.data['token'],
                'profile_id': profile.id,
                'has_jorang': has_jorang,
                'jorang': {
                    'nickname': jorang_nickname,
                    'color': jorang_color
                },
                'today_post_id': today_post_id
            }
        })


# TODO: 없애되기는 히지만, 계속 놔두는게 개발에 도움이 될 것.
# / 로그인 되었나 확인 하는 용도
@api_view(['GET'])
@permission_classes([MyIsAuthenticated, ])
def login_test(request):
    """
        JWT 검증 -> config.permission.MyIsAuthenticated(요기서 Response 결정)
        -> login_test 잘되었으면, 성공되었다고 돌려보내준다.

        JWT token 을 통해서 미리 인증을 하는 과정을 거치고,
        만약 통과를 할 경우, 바로 Response 로 보낸다.
    """
    return Response({'message': '로그인 성공'})
