from datetime import date

from rest_framework.views import APIView
from rest_framework.response import Response

from core.serializers import AttendanceSerializer
from core.models import Attendance, Profile
from config.permissions import MyIsAuthenticated


class AttendanceView(APIView):
    permission_classes = [MyIsAuthenticated, ]

    def get(self, request):
        """
        TODO: 언제 추가가 되는지 확인을 해야겠다.
        Profile 이 이번달에 출석을 한 일수를 계산을 하기 위해서 만든 API 입니다.

        :param request:
        :return:
        """
        email = request.user.email
        profile = Profile.objects.get(email=email)
        attendances_of_this_month = Attendance.objects.filter(
            profile=profile, date__year=date.today().year, date__month=date.today().month)
        serializer = AttendanceSerializer(attendances_of_this_month, many=True)

        return Response(serializer.data)
