from rest_framework import serializers as sz
from django.contrib.auth import get_user_model


class ProfileSerializer(sz.ModelSerializer):
    password = sz.CharField(write_only=True)

    def create(self, validated_data):
        Profile = get_user_model()
        profile = Profile.objects.create_user(**validated_data)
        return profile

    class Meta:
        model = get_user_model()
        fields = [
            'username',
            'password',
            'email',
            'nickname'
        ]
