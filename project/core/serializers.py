from rest_framework import serializers as sz
from core.models import Profile, UserCoin, Attendance, UserFeedback, FirebaseUID
from shop.serializers import ItemSerializer
from core.ERROR.error_cases import GlobalErrorMessage400


class ProfileSerializer(sz.ModelSerializer):
    password = sz.CharField(write_only=True)

    def create(self, validated_data):
        profile = Profile.objects.create_user(**validated_data)
        return profile

    class Meta:
        model = Profile
        fields = [
            'password',
            'email',
        ]


class SignUpSerializer(sz.Serializer):
    email = sz.EmailField()
    password = sz.CharField(write_only=True)
    uid = sz.CharField(write_only=True)

    def create(self, validated_data):
        uid = validated_data.pop("uid", None)
        if uid:
            profile = Profile.objects.create_user(**validated_data)
            FirebaseUID.objects.create(
                profile=profile,
                uid=uid
            )
            return profile
        raise GlobalErrorMessage400("Firebase Token을 보내주세요.")

    class Meta:
        model = Profile
        fields = [
            'password',
            'email',
            'uid'
        ]


class UserCoinSerializer(sz.ModelSerializer):
    profile = sz.SlugRelatedField(queryset=Profile.objects.all(), slug_field='email')

    def create(self, validated_data):
        return UserCoin.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.coin = validated_data.get('coin', instance.coin)
        instance.last_date = validated_data.get('last_date', instance.last_date)
        return instance

    class Meta:
        model = UserCoin
        fields = [
            'profile',
            'last_date',
            'coin',
        ]


class AttendanceSerializer(sz.ModelSerializer):
    class Meta:
        model = Attendance
        fields = [
            'date',
            'emotion'
        ]


class UserFeedbackSerializer(sz.ModelSerializer):
    class Meta:
        model = UserFeedback
        fields = "__all__"


class ProfileDetailResSerializer(sz.Serializer):
    email = sz.EmailField()
    title = sz.CharField()
    jorang_nickname = sz.CharField()
    jorang_items = ItemSerializer()
    jorang_status = sz.CharField()
    user_continuity = sz.IntegerField()
    user_coin = sz.IntegerField()

    class Meta:
        fields = [
            'email',
            'title',
            'jorang_nickname',
            'jorang_items',
            'jorang_status',
            'user_continuity',
            'user_coin'
        ]


class ProfileDetailReqSerializer(sz.Serializer):

    title = sz.CharField()
    jorang_nickname = sz.CharField()

    class Meta:
        fields = [
            'email',
            'title',
            'jorang_nickname',
            'jorang_items',
            'jorang_status',
            'user_continuity',
            'user_coin'
        ]
