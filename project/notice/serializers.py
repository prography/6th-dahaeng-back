from rest_framework import serializers as sz
from .models import Notice


class NoticeSerializer(sz.ModelSerializer):
    class Meta:
        model = Notice
        fields = '__all__'
