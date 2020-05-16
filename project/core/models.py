from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):
    user_in_migrations = True

    def create_user(self, username, email, nickname, password=None):
        if not email:
            raise ValueError('이메일은 필수입니다.')
        # 가독성을 고려하여 kwargs 사용 안함
        user = self.model(
            username=username,
            email=self.normalize_email(email),
            nickname=nickname
        )
        user.set_password(password)
        user.status = '0'
        user.role = '0'
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, nickname="", password=None):
        user = self.create_user(
            username=username,
            email=email,
            password=password,
            # 관리자의 경우 nickname이 필요없지만 unique해야하므로 username을 nickname으로 사용
            nickname=username
        )
        user.status = '1'
        user.role = '10'
        user.save(using=self._db)
        return user


class Profile(AbstractBaseUser, PermissionsMixin):
    objects = UserManager()

    STATUS_CHOICES = (
        ('0', '가입대기'),
        ('1', '가입활성화'),
        ('8', '블랙리스트'),
        ('9', '탈퇴')
    )

    ROLE_CHOICES = (
        ('0', '일반 유저'),
        ('10', '관리자')
    )

    username = models.CharField(max_length=16, unique=True)
    email = models.EmailField(max_length=50)
    nickname = models.CharField(max_length=10, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, blank=True)
    role = models.CharField(max_length=2, choices=ROLE_CHOICES, blank=True)

    @property
    def is_staff(self):
        return self.role == '10'

    @property
    def is_superuser(self):
        return self.role == '10'

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
