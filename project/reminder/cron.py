from .models import Reminder
from django.contrib.auth import get_user_model
from record.models import Post
from .serializers import ReminderSerializer
from datetime import date


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
