from django.urls import path
from . import views

urlpatterns = [
    path('', views.NoticeView.as_view()),
    path('reminder/', views.NoticeAndReminderView.as_view()),
]
