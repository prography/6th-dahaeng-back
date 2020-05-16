from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from .serializers import ProfileSerializer
from django.contrib.auth import get_user_model
from config.permissions import MyIsAuthenticated

# email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_text
from .tokens import account_activation_token
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode


class CreateProfileView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        queryset = get_user_model().objects.all()
        serializer = ProfileSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        """
        {
            "profile": {
                "username": "rkdalstjd9",
                "password": "qwe123",
                "email": "rkdalstjd9@naver.com",
                "nickname": "arkss"
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
            'message': serializer.data
        })


@api_view(['GET'])
@permission_classes([MyIsAuthenticated, ])
def login_test(request):
    return Response({'message': '로그인 성공'})


@api_view(['POST'])
@permission_classes([AllowAny, ])
def send_email_for_active(request):
    """
    {
        'username': 'rkdalstjd9'
    }
    """
    username = request.data.get('username')
    if not username:
        return Response({
            'response': 'error',
            'message': 'username 파라미터가 없습니다.'
        })

    User = get_user_model()
    try:
        profile = User.objects.get(username=username)
    except:
        return Response({
            'response': 'error',
            'message': f'{username}이 존재하지 않습니다.'
        })
    # 프론트, 백앤드 서버가 나뉘어 있어서 current_site가 의미가 없다.
    #current_site = get_current_site(request)
    message = render_to_string(
        'core/email_for_active.html',
        {
            # 'domain': current_site.domain,
            'profile_id': urlsafe_base64_encode(force_bytes(profile.id)).encode().decode(),
            'token': account_activation_token.make_token(profile),
        }
    )

    mail_title = "[다행] 회원가입 인증 메일입니다."
    user_email = profile.email
    email = EmailMessage(
        mail_title,
        message,
        to=[user_email]
    )
    email_result = email.send()
    if email_result:
        return Response({
            'response': 'success',
            'message': '메일 전송에 성공하였습니다.'
        })
    else:
        return Response({
            'response': 'error',
            'message': '메일 전송에 실패하였습니다.'
        })


@api_view(['POST'])
@permission_classes([AllowAny, ])
def user_active(request):
    """
    {
        'profile_id64': profile_id64,
        'token': token
    }
    """

    profile_id64 = request.data.get('profile_id64')
    token = request.data.get('token')

    if profile_id64 is None or token is None:
        return Response({
            'response': 'error',
            'message': ''
        })
    profile_id = int(force_text(urlsafe_base64_decode(profile_id64)))
    User = get_user_model()
    try:
        profile = User.objects.get(id=profile_id)
    except:
        return Response({
            'response': 'error',
            'message': f'{profile_id}에 해당하는 유저가 없습니다.'
        })

    if account_activation_token.check_token(profile, token):
        profile.status = '1'
        profile.save()
    else:
        return Response({
            'response': 'error',
            'message': '유효하지 않은 token입니다.'
        })

    return Response({
        'response': 'success',
        'message': f'{profile}이 활성화 되었습니다.'
    })
