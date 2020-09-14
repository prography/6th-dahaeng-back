from storages.backends.s3boto3 import S3Boto3Storage
from config.settings.prod import AWS_STORAGE_BUCKET_NAME, AWS_REGION, AWS_S3_CUSTOM_DOMAIN, \
    AWS_DEFAULT_ACL


class MediaStorage(S3Boto3Storage):
    file_overwrite = False
    default_acl = AWS_DEFAULT_ACL
    bucket_name = AWS_STORAGE_BUCKET_NAME
    region_name = AWS_REGION
    custom_domain = AWS_S3_CUSTOM_DOMAIN
