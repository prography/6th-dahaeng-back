from storages.backends.s3boto3 import S3Boto3Storage
from config.settings import AWS_STORAGE_BUCKET_NAME, AWS_REGION, AWS_S3_CUSTOM_DOMAIN, MEDIAFILES_LOCATION, AWS_DEFAULT_ACL

class MediaStorage(S3Boto3Storage):
    location = MEDIAFILES_LOCATION
    file_overwrite = False
    default_acl = AWS_DEFAULT_ACL
    bucket_name = AWS_STORAGE_BUCKET_NAME
    region_name = AWS_REGION
    custom_domain = AWS_S3_CUSTOM_DOMAIN