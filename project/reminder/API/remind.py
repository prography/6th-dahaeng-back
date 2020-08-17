from rest_framework.views import APIView
from rest_framework.response import Response
from config.permissions import MyIsAuthenticated
from record.models import Post

from reminder.models import Reminder
from reminder.serializers import ReminderSerializer

from datetime import date


class ReminderView(APIView):
    permission_classes = [MyIsAuthenticated, ]

    # TODO: 사용자가 하루에 한 번씩 요청을 보내는 것 보다는 cronjob으로 바꾸자.
    # TODO: 날짜 계산을 어떻게 해야하지? 단순히 7일전 30일전 365일전?
    def get(self, request, *args, **kwargs):
        """
            오늘 다시 알려줄 Remind 가 있는지 확인을 하고,
            있으면, 그것들을 정래허 돌려준다.
        """
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
        """
            [2, 7, 30, 365] 에 대해서,
            오늘 과 위 list 안에 있는 것 만큼 차이가 나게 될 경우,
            그것글을 reminder 에 추가를 한다.
            그리고, 그것을 Get 을 통해서, 내가 이런것도 작성했지 하고 보게한다.


        """
        profile = request.user
        today = date.today()
        posts = Post.objects.filter(profile=profile)
        event_days = [2, 7, 30, 365]
        for post in posts:
            post_created_at = post.created_at
            interval = (today - post_created_at).days
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
