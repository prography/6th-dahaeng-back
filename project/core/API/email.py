"""
    본인 인증 Email 을 보내기 위한, 함수입니다.
"""
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from core.API.tokens import account_activation_token


def send_email_for_active(profile, request):
    """
        /signup/ 할 때, 사용하기 위해서 만든 것으로,
        gmail 을 통해서, 사용자가 입력한 email 에 대해서,
        확인하는 용도로 사용되는 함수입니다.

        profile_id 와 token 을 건네주어, 메일을 보내는 용도로 사용이 됩니다.
    """
    # 프론트, 백앤드 서버가 나뉘어 있어서 current_site 가 의미가 없다.
    # current_site = get_current_site(request)

    # TODO: 나중에, 버튼으로 간편하게 이동 할 수 있도록 구현을 해야겠다.
    # TODO: Celery 로 바꾸어서 구현을 하자. - by 경준.
    message = render_to_string(
        'core/email_for_active.html',
        {
            'profile_id': urlsafe_base64_encode(force_bytes(profile.id)),
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
    return email_result
