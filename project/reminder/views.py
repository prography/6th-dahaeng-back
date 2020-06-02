
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework_jwt.utils import jwt_decode_handler
from config.permissions import MyIsAuthenticated
from record.models import Post
from .serializers import ReminderSerializer
from .models import Reminder
from datetime import date


class ReminderView(APIView):
    # TODO: 사용자가 하루에 한 번씩 요청을 보내는 것 보다는 cronjob으로 바꾸자.
    # TODO: 날짜 계산을 어떻게 해야하지? 단순히 7일전 30일전 365일전?
    def get(self, request, *args, **kwargs):
        profile = request.user
        queryset = Reminder.objects.filter(
            post__profile=profile,
            created_at=date.today()
        )
        serializer = ReminderSerializer(queryset, many=True)
        return Response({
            'response': 'success',
            'message': serializer.data
        })

    def post(self, request, *args, **kwargs):
        profile = request.user
        today = date.today()
        posts = Post.objects.filter(profile=profile)
        event_days = [1, 7, 30, 365]
        for post in posts:
            post_created_at = post.created_at
            interval = (today-post_created_at).days
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

        return Response({
            'response': 'success',
            'message': 'reminder를 생성하였습니다.'
        })
