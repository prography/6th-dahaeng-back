from rest_framework import serializers as sz
from django.contrib.auth import get_user_model
from core.models import Profile, UserCoin, Attendance


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
    """
        아래 코드느 profile 을 data 라는 parameter 로 input 으로 받고,
        .is_valid() 이후, validated_data 로 변경이 되었습니다.
        그후, default 값을 활용을 하여,
        .save() 를 통해서, create 와 update 를 통해 진행됩니다.
    """
    profile = sz.SlugRelatedField(queryset=Profile.objects.all(), slug_field='email')

    def create(self, validated_data):
        """
        profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
        이것을 바탕으로 보았을 때, 바로 저 Profile 객체를 지칭을 하여 넘겨주어야 할 필요성이 있어 보인다.

        :param validated_data: {'profile': <Profile: test1@naver.com>}
         이고, 그 이외의 값의 경우 model.UserCoin 의 default 값으로 변경이 됩니다.
        :return:
        """
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
