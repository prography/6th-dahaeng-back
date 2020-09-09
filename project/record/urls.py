"""
질문 생성 및 List 접근
/questions GET 질문 List 를 관리자로써 접근을 할 수 있다.
/questions POST 관리자로서 질문을 생성한다.

----------------------------------------------------------------
1. questions/
이를 통해서 관리자가 질문을 생성을 한다
2. posts/questions/
이를 통해서 매일 유저들에게 Post 객체를 생성 할 수 았도록 user 와 question 을 매칭 가능할 수 있게한다.
3. posts/
하루에 한번 Post 객체를 생성을 할 수 있도록 한다. Get or Create
4. posts/<int:pk>/
하나의 객체에 접근을 하여 detail get patch delete 를 할 수 있도록 한다.

"""
from django.urls import path

from .API import question
from .API import post

urlpatterns = [
    # 관리자의 질문생성
    path('questions/', question.QuestionView.as_view(), name='question_list'),
    # 하루당 한번씩, User 에게 Question 을 주어야 한다.
    path('posts/questions/', post.everyday_user_question_generation, name='user_question_generation'),
    # post 의 생성과 search
    path('posts/', post.PostView.as_view(), name='post_get_create'),
    # post Detail
    path('posts/<int:pk>/', post.PostDetail.as_view(), name='post_detail'),


]
