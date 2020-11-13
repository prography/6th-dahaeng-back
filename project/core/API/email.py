"""
    본인 인증 Email 을 보내기 위한, 함수입니다.
"""
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import get_template




def send_email_for_active(profile, request):
    """
        /signup/ 할 때, 사용하기 위해서 만든 것으로,
        gmail 을 통해서, 사용자가 입력한 email 에 대해서,
        확인하는 용도로 사용되는 함수입니다.

        profile_id 와 token 을 건네주어, 메일을 보내는 용도로 사용이 됩니다.
    """

    # TODO: Celery 로 바꾸어서 구현을 하자. - by 경준.
    authentication_information = {
        'profile_id': profile.id,
        'token': profile.email_token.token,
    }
    message = get_template('core/email_for_active.html').render(authentication_information)

    mail_title = "[다행] 회원가입 인증 메일입니다."
    user_email = profile.email
    email = EmailMessage(
        mail_title,
        message,
        to=[user_email]
    )
    email.content_subtype = "html"
    email_result = email.send()
    return email_result
