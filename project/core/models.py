from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):
    user_in_migrations = True

    def create_user(self, email, password=None):
        if not email:
            raise ValueError('이메일은 필수입니다.')
        # 가독성을 고려하여 kwargs 사용 안함
        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        # TODO: 이메일 인증 잠시 보류
        user.status = '1'
        user.role = '0'
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(
            email=email,
            password=password,
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

    SOCIAL_CHOICES = (
        ("KAKAO", "kakao"),
        ("NAVER", "naver"),
        ("APPLE", "apple"),
        ("NONE", "none")
    )

    email = models.EmailField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, blank=True)
    role = models.CharField(max_length=2, choices=ROLE_CHOICES, blank=True)
    social = models.CharField(
        max_length=20, choices=SOCIAL_CHOICES, null=True, blank=True, default="NONE")

    @property
    def is_staff(self):
        return self.role == '10'

    @property
    def is_superuser(self):
        return self.role == '10'

    @property
    def is_active(self):
        return self.status == '1'

    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['nickname']

    def __str__(self):
        return self.email


class Jorang(models.Model):
    STATUS_CHOICES = (
        ('0', '알'),
        ('1', '유년기'),
        ('2', '성장기'),
        ('3', '성숙기')
    )

    nickname = models.CharField(max_length=50)
    color = models.CharField(max_length=6, help_text='16진수 코드 6개 ex) FFFFFF')
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default=0)
    profile = models.OneToOneField(
        Profile, null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, default="Da:haeng")

    def __str__(self):
        return "[%s] %s (%s)" % (self.profile, self.nickname, self.title)


class UserCoin(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    last_date = models.DateField(null=True)
    coin = models.PositiveIntegerField(default=0)


class Attendance(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    date = models.DateField(null=False)
    emotion = models.CharField(max_length=10, null=True)

    def __str__(self):
        return "(%s) %s" % (self.date, self.profile)

    class Meta:
        unique_together = ('profile', 'date')
        ordering = ['date']
