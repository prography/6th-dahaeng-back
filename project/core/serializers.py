from rest_framework import serializers as sz
from django.contrib.auth import get_user_model
from core.models import Profile, UserCoin

class ProfileSerializer(sz.ModelSerializer):
    password = sz.CharField(write_only=True)

    def create(self, validated_data):
        Profile = get_user_model()
        profile = Profile.objects.create_user(**validated_data)
        return profile

    class Meta:
        model = get_user_model()
        fields = [
            'password',
            'email'
        ]


class UserCoinSerializer(sz.ModelSerializer):
    profile = sz.SlugRelatedField(queryset=Profile.objects.all(), slug_field='email')

    class Meta:
        model = UserCoin
        fields = [
            'profile',
            'coin',
        ]