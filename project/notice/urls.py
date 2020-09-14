"""
Notice 는 관리자가 공지를 하기위해서 만든 것으로,

아직 까지 필요하지 않은 기능이라
원래 있던 대로 구현을 하기는 하였으나,
추후 좀더 공부를 통해서
추가 설명이 작성이 필요.

#TODO: Reminder serializer 부분도 궁금하네

"""
from django.urls import path
from .API import notice

urlpatterns = [
    path('', notice.NoticeView.as_view()),
    path('reminder/', notice.NoticeAndReminderView.as_view()),
]
