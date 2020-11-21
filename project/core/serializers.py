from rest_framework import serializers as sz
from core.models import Profile, UserCoin, Attendance, UserFeedback


class ProfileSerializer(sz.ModelSerializer):
    password = sz.CharField(write_only=True)

    def create(self, validated_data):
        profile = Profile.objects.create_user(**validated_data)
        return profile

    class Meta:
        model = Profile
        fields = [
            'password',
            'email'
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
