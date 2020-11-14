from django.contrib.auth import get_user_model
from datetime import date
from rest_framework.response import Response
from reminder.models import Reminder
from reminder.serializers import ReminderSerializer
from record.models import Post


def create_reminder():
    today = date.today()
    print(f"create {today} reminder")

    event_days = [1, 7, 30, 365]
    posts = Post.objects.all()
    for post in posts:
        interval = (today-post.created_at).days
        if interval in event_days:
            data = {
                'post': post.id,
                'interval': interval
            }
            serializer = ReminderSerializer(data=data)
            if serializer.is_valid():
                reminder = serializer.save()
            else:
                return Response({
                    'response': 'error',
                    'message': serializer.errors
                })


def push_reminder():
    """
        서버에서 일정한 시간이 되면 클라이언트에 데이터 푸쉬
    """
    pass