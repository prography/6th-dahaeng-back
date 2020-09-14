"""
개발용 설정입니다.


"""

from config.settings.commons import *

DEBUG = True

"""
                                    DB 설정 
                    추후 다른 서버로 옮기게 될 경우, 이부분을 바꾸어야한다.
    현재 다행 재설계 단계에 있어, localhost 에서 진행을 하는 중이며 추후 다른 방식으로 변경 될 가능성이 많다.
"""

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
