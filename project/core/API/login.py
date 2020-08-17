"""
Profile 의
login, signup, JWT 등 관련된 부분들을 구현을 해두었다.

"""
from datetime import date

from django.contrib.auth import get_user_model
from django.contrib.auth.models import update_last_login

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_jwt.views import ObtainJSONWebToken
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes

from core.models import Jorang
from core.serializers import ProfileSerializer, UserCoinSerializer
from config.permissions import MyIsAuthenticated

from record.serializers import UserQuestionSerializer
from record.models import UserQuestion

# /sighup/ 회원 가입
class CreateProfileView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        """
        TODO: 제거 필요, 모든 사용자가 Email 에 접근을 해야할 필요성은 없음. 그렇기 때문에, 지워두어야 할 필요성이 있음.
        모든 사용자의 EMAIL 을 접근을 하여, 들고옴.

        :param request: rest_framework.request.Request
        :param args: ()
        :param kwargs: {}
        :return:
        """
        queryset = get_user_model().objects.all()
        serializer = ProfileSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        """
        TODO: 이메일 전송이 실패하면 생성된 유저도 무효시키도록 트렌젝션 필요
        answer  그렇다면, Email 을 보내고 난 뒤에 생성을 하면 되는 문제 아닌가?
        아니면, try catch final 구조를 통해서, final 에 user 를 생성을 시킵시다.

        신규 사용자의 email 과 password 를 받아.
        새로운 Profile 을 만들어준다.
        {
            "profile": {
                "email": "rkdalstjd9@naver.com",
                "password": "qwe123"
            }
        }
        """

        data = request.data.get('profile')
        if not data:
            return Response({
                'response': 'error',
                'message': 'profile 파라미터가 없습니다.'
            })
        serializer = ProfileSerializer(data=data)
        if serializer.is_valid():
            profile = serializer.save()
        else:
            return Response({
                'response': 'error',
                'message': serializer.errors
            })

        return Response({
            'response': 'success',
            'message': '회원가입이 완료되었습니다.'
        })

        # TODO: milestone2
        """
        email_result = send_email_for_active(profile, request)

        if email_result:
            return Response({
                'response': 'success',
                'message': '이메일을 전송하였습니다.'
            })
        else:
            return Response({
                'response': 'error',
                'message': '이메일을 전송에 실패하였습니다.'
            })
        """


# /login/
class MyObtainJSONWebToken(ObtainJSONWebToken):
    def post(self, request):
        """
            로그인을 위해서 구현된 모델이며,
            request.user 의 경우 AnonymousUser 인 상태로 input 이 들어오는 상태이며,


        :param request: rest_framework.request.Request
        :return: rest_framework.response.Response
        """
        response = super().post(request, content_type='application/json')

        if response.status_code != 200:
            return Response({
                'response': 'error',
                'message': '로그인이 실패하였습니다.'
            })
        is_first_login = False
        User = get_user_model()
        email = request.data.get('email', '')
        try:
            profile = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({
                'response': 'error',
                'message': '유효하지않은 계정입니다.'
            })

        print("profile.last_login", profile.last_login)

        if profile.last_login is None:

            is_first_login = True
            serializer = UserQuestionSerializer(
                data={"profile": email}, partial=True)
            if serializer.is_valid():
                serializer.save()

            usercoinSerializer = UserCoinSerializer(data={"profile": email})
            if usercoinSerializer.is_valid():
                print("usercoinSerializer", usercoinSerializer)
                usercoinSerializer.save()

        else:

            userq = UserQuestion.objects.get(profile=profile.id)
            serializer = UserQuestionSerializer(
                userq, data={"last_login": date.today()}, partial=True)
            if serializer.is_valid():
                serializer.save()


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


# / 로그인 되었나 확인 하는 용도
@api_view(['GET'])
@permission_classes([MyIsAuthenticated, ])
def login_test(request):
    """
        JWT 검증 -> MyIsAuthenticated(요기서 Response 결정)
        -> login_test 잘되었으면, 성공되었다고 돌려보내준다.

        JWT token 을 통해서 미리 인증을 하는 과정을 거치고,
        만약 통과를 할 경우, 바로 Response 로 보내
        :param request:
        :return:
    """
    return Response({'message': '로그인 성공'})
