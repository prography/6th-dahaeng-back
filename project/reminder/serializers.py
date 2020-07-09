from rest_framework import serializers as sz
from record.serializers import PostSerializer
from .models import Reminder
from record.models import Post


class ReminderSerializer(sz.ModelSerializer):
    posts = sz.SerializerMethodField()

    def get_posts(self, obj):
        post = obj.post
        try:
            question_content = post.question.content
        except:
            question_content = None

        return {
            'emotion': post.emotion,
            'detail': post.detail,
            'question': question_content,
            'image': post.image.url
        }

    class Meta:
        model = Reminder
        fields = ['post', 'interval', 'created_at',  'posts']
