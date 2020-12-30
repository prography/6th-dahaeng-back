"""
    프로젝트의 메인으로서의 기능을 담당하기 위해서 만든 모델들을 구현을 해두었다.

    Profile(Custom User model) -> UserManager, Profile
    Jorang -> 우리의 마스코트 조랭이.
    UserCoin -> 사용자의 코인 값을 저장하기 위해서 만든 모델.
    Attendance -> 사용자의 출석을 체크하기 위해서 만든 모델이다.
"""
import uuid

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):
    user_in_migrations = True

    def create_user(self, email, password=None, social="NONE"):
        if not email:
            raise ValueError('이메일은 필수입니다.')
        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)

        user.email_token = EmailToken.objects.create(token=str(uuid.uuid4()))

        user.status = '0'
        user.role = '0'
        user.social = social
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(
            email=email,
            password=password,
        )
        user.status = '1'
        user.role = '10'
        user.social = "None"
        user.save(using=self._db)
        return user


class Profile(AbstractBaseUser, PermissionsMixin):
    """
        Custom User Model 을 구현 하기 위해서는 BaseUserManager, AbstractBaseUser 를 상속을 받아 구현을 해야한다.
        Profile 을 통해서 Custom User 모델을 표현을 하고자 사용을 하였으며,
        objects = UserManage() 을 통해서 위에 정의를 해둔 함수들을 활용을 한다.
        USERNAME_FIELD = 'email' 이라고 명시함을 통해서, 확실학게 이해를 할 수 있다.

        TODO: SOCIAL_CHOICES 를 해결을 해야한다. 이 부분에 대해서 추가로 구현을 해두어야 할 필요성이 있다.
    """
    objects = UserManager()
    USERNAME_FIELD = 'email'

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
    email_token = models.OneToOneField('EmailToken', null=True, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # 모든 유저는 가입대기 부터 시작한다.
    status = models.CharField(
        max_length=2, choices=STATUS_CHOICES, blank=True, default='0')
    role = models.CharField(
        max_length=2, choices=ROLE_CHOICES, blank=True, default='0')
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

    def __str__(self):
        return self.email


class FirebaseUID(models.Model):
    profile = models.OneToOneField(Profile, primary_key=True, on_delete=models.CASCADE)
    uid = models.CharField(
        unique=True,
        max_length=300,
        verbose_name='유저 UID (Firebase 에서 자동 생성)'
    )


class EmailToken(models.Model):
    token = models.CharField(default="", max_length=37)


class Jorang(models.Model):
    """
        우리의 마스코트 조랭이
        조랭이의 경우, 생성될 때, 유저와 1:1 [OneToOneField] 로 mapping 이 되기 떄문에
        유저 당 딱 한번 밖에 생성이 되지 않는다.
        그렇기에 유의를 할 필요가 있다.
    """
    STATUS_CHOICES = (
        ('0', '알'),
        ('1', '유년기'),
        ('2', '성장기')
    )

    profile = models.OneToOneField(
        Profile, null=True, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=50)
    color = models.CharField(max_length=6, help_text='16진수 코드 6개 ex) FFFFFF')
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default=0)
    title = models.CharField(max_length=100, default="Da:haeng")

    def __str__(self):
        return "[%s] %s (%s)" % (self.profile, self.nickname, self.title)


class UserCoin(models.Model):
    """
        코인 지급과 관련해서, Profile 의 updated_at 과 관련해서 이슈가 있어서
        이를 해결 하기위해서, 만든 모델입니다.
        profile 과 1대1 OneToOneField 로 구현을 함으로써, Profile 에 대한 코인 값을 설정을 할 수 있다.
    """
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    last_date = models.DateField(null=True)
    coin = models.PositiveIntegerField(default=0)


class Attendance(models.Model):
    """
        1:N relation 이며,
        하나의 Profile(USER) 에 대해서, N 개의 출석이 있을 것이고,
        그 출석들을 저장을 하기위해서 만든 모델입니다.

        출석은 record.models.Post 객체를 생성을 할 때, 출석을 하였다고 판단을 합니다.
    """
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    date = models.DateField(null=False)
    emotion = models.CharField(max_length=10, null=True)

    def __str__(self):
        return "(%s) %s" % (self.date, self.profile)

    class Meta:
        unique_together = ('profile', 'date')
        ordering = ['date']


class PushNotificationMessage(models.Model):
    MESSAGE_CHOICES = (
        ('h', "happy word"),
        ('r', "reminder word")
    )

    content = models.CharField(max_length=200, null=False)
    type = models.CharField(max_length=2, choices=MESSAGE_CHOICES, default='h')

    def __str__(self):
        return "[{}]{}".format(self.type, self.content)


class UserFeedback(models.Model):
    feedback = models.TextField()
