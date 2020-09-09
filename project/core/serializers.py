from rest_framework import serializers as sz
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
        SlugRelatedField 를 통해서, queryset 을 통해서 들고온 List 와 slug_field=email 에서  비교를 통해,
        {profile: shrldh3576@naver.com} 을 비교를 하여,
        Email 필드와 비교를 하여, 같은 인자를 찾아서
        데이터를 정제하여, Profile 객체 형태로 validated_data 에 넣어서 보내준다.

        :param validated_data: {'profile': <Profile: test1@naver.com>}
         이고, 그 이외의 값의 경우 model.UserCoin 의 default 값으로 변경이 됩니다.
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
