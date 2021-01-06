from rest_framework import serializers as sz
from shop.serializers import ItemSerializer


class LoginJorangSerializer(sz.Serializer):
    nickname = sz.CharField(max_length=50)
    items = ItemSerializer(many=True)


class LoginSerializer(sz.Serializer):
    token = sz.CharField()
    profile_id = sz.CharField()
    has_jorang = sz.BooleanField()
    jorang = LoginJorangSerializer()
    today_post_id = sz.IntegerField()


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
