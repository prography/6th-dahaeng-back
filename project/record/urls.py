"""
REST 란?
HTTP URI(Uniform Resource Identifier)를 통해 자원(Resource)을 명시하고,
 HTTP Method(POST, GET, PUT, DELETE)를 통해 해당 자원에 대한 CRUD Operation을 적용하는 것을 의미한다.

TODO: 관리자만, 질문을 생성 및 접근을 할 수 있는데, 이 부분을 확인을 하고 싶다.
질문 생성 및 List 접근
/questions GET 질문 List 를 관리자로써 접근을 할 수 있다.
/questions POST 관리자로서 질문을 생성한다.

----------------------------------------------------------------

원래
path('posts/newpost/', post.PostCreateView.as_view(), name='post_create'),
path('posts/', views.PostList.as_view(), name='post_list'),
path('posts/<int:pk>/', views.PostDetail.as_view(), name='post_detail'),

-> 수정 구상본
posts/question/ -> FBV 로 GET method 하나만 따로 정의| user_question 생성
posts/ -> get search 할수 있는 기능을 따로 넣어주어야 원래 있는 기능과 모순이 안 생김, 원래대로 구현 예정
posts/ -> create
posts/<int:pk> -> detail | get put delete

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
