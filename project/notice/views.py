from rest_framework.views import APIView
from .models import Notice, Read
from .serializers import NoticeSerializer


class NoticeView(APIView):
    def get(self, request, *args, **kwargs):
        profile = request.user
        queryset = Notice.objects.filter(
            related_read__is_read=False,
            related_read__profile=profile
        )
        serializer = NoticeSerializer(queryset, many=True)
        return Response(serializer.data)
