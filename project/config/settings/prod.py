"""
배포용 설정입니다.

pip install psycopg2

"""
import os
from config.settings.commons import *

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': '디비이름',
        'USER': '유저이름',
        'PASSWORD': '비밀번호',
        'HOST': '엔드포인트',
        'PORT': '5432',
    }
}

# AWS S3 Storage
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# AWS Access
AWS_ACCESS_KEY_ID = get_secret('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = get_secret('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = get_secret('AWS_STORAGE_BUCKET_NAME')
AWS_REGION = get_secret('AWS_REGION')
AWS_S3_CUSTOM_DOMAIN = '%s.s3.%s.amazonaws.com' % (
    AWS_STORAGE_BUCKET_NAME, AWS_REGION)
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
AWS_DEFAULT_ACL = 'public-read'
AWS_MEDIA_LOCATION = 'media'
MEDIA = 'http://%s/%s' % (AWS_S3_CUSTOM_DOMAIN, AWS_MEDIA_LOCATION)
