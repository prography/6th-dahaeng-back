from rest_framework.views import APIView
from rest_framework.response import Response
from notice.models import Notice, Read
from notice.serializers import NoticeSerializer
import datetime

# from reminder.models import Reminder
# from reminder.serializers import ReminderSerializer


class NoticeView(APIView):
    def get(self, request, *args, **kwargs):
        profile = request.user
        queryset = Notice.objects.filter(
            expired_at__gt=datetime.date.today()
        )
        serializer = NoticeSerializer(queryset, many=True)
        return Response({
            'response': 'success',
            'message': serializer.data
        })


class NoticeAndReminderView(APIView):
    def get(self, request, *args, **Kwargs):
        profile = request.user
        notice_queryset = Notice.objects.filter(
            expired_at__gt=datetime.date.today()
        )
        # reminder_queryset = Reminder.objects.filter(
        #     post__profile=profile,
        #     created_at=datetime.date.today()
        # )

        notice_serializer = NoticeSerializer(notice_queryset, many=True)
        # reminder_serializer = ReminderSerializer(reminder_queryset, many=True)

        return Response({
            'response': 'success',
            'notice': notice_serializer.data,
            # 'reminder': reminder_serializer.data
        })
