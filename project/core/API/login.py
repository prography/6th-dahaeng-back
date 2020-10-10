"""
Profile 의
login, signup, JWT 등 관련된 부분들을 구현을 해두었다.

signup -> user_active -> login


"""
# third
from datetime import date

# Django
from django.contrib.auth.models import update_last_login
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
from core.API.tokens import account_activation_token
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
@api_view(['POST'])
@permission_classes([AllowAny, ])
def user_active(request):
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

    profile_id64 = request.data.get('profile_id64')
    token = request.data.get('token')

    if profile_id64 is None or token is None:
        raise GlobalErrorMessage("profile_id64 or token 이 존재하지 않습니다.")

    profile_id = int(force_text(urlsafe_base64_decode(profile_id64)))
    try:
        profile = Profile.objects.get(id=profile_id)
    except Profile.DoesNotExist:
        raise GlobalErrorMessage(f' profile pk= {profile_id}에 해당하는 유저가 없습니다.')

    if account_activation_token.check_token(profile, token):
        profile.status = '1'
        profile.save()
    else:
        raise GlobalErrorMessage('유효하지 않은 token 입니다.')

    return Response({
        'response': 'success',
        'message': f'{profile}이 활성화 되었습니다.'
    })


# /login/
class MyObtainJSONWebToken(ObtainJSONWebToken):
    def post(self, request):
        """
            ObtainJSONWebToken 을 상속을 받아
            super.post() 를 통해, token 을 할당을 받을 수 있다.

            1. 계정 활성화 check
            2. jwt_token 얻기
            3-1. 처음 로그인 경우
            -> 우선 회원가입을 하면서, User Question 을 만들어 주고, profile_id 만 만들어 준다.
                추후, [매일 question user 매칭을 만드는 API 를 통해서, 이어준다.]
            3-2. 아닐 경우
            -> user_question 에 last_login 을 update 해두어서,
                하루에 질문 update 를 위헤서 두세번 같은 작업을 반복하도록 하지 않는다. -> 하루에 한번만 질문을 update 해야한다.
            4. 조랭이 check

            serializer.is_valid() 를 통해서
            data ={profile: email.com} 에 넣어둔 email 을 Profile 내부에 있는 queryset 과 비교를 해서,
            만들었다고 볼 수 있겠다고 생각한다.
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
        if str(profile.last_login).split()[0] < date.today():
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

        return Response({
            'response': 'success',
            'message': {
                'token': response.data['token'],
                'profile_id': profile.id,
                'has_jorang': has_jorang,
                'jorang': {
                    'nickname': jorang_nickname,
                    'color': jorang_color
                }
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
