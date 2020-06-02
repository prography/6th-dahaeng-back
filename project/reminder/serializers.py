from rest_framework import serializers as sz
from record.serializers import PostSerializer
from .models import Reminder
from record.models import Post


class ReminderSerializer(sz.ModelSerializer):
    posts = sz.SerializerMethodField()

    def get_posts(self, obj):
        return {
            'emotion': obj.post.emotion,
            'detail': obj.post.detail,
            'question': obj.post.question.content
        }

    class Meta:
        model = Reminder
        fields = ['post', 'interval', 'created_at',  'posts']
