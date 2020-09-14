"""
리마인더는 7일/30일/365일 전의 일기를 다시 꺼내볼수잇도록 알람주는거에요

아직 까지 필요하지 않은 기능이라
원래 있던 대로 구현을 하기는 하였으나,
추후 좀더 공부를 통해서
추가 설명이 작성이 필요.

#TODO: Reminder serializer 부분도 궁금하네

"""
from django.urls import path
from .API import remind


urlpatterns = [
    path('', remind.ReminderView.as_view(), name="reminder"),
]
