from rest_framework import serializers as sz


class LoginJorangSerializer(sz.Serializer):
    nickname = sz.CharField(max_length=50)
    color = sz.CharField()


class LoginSerializer(sz.Serializer):
    token = sz.CharField()
    profile_id = sz.CharField()
    has_jorang = sz.BooleanField()
    jorang = LoginJorangSerializer()
    today_post_id = sz.IntegerField()
