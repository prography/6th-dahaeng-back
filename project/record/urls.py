from django.urls import path
from . import views

urlpatterns = [
    path('posts/create/', views.PostCreateView.as_view(), name='post_create'),
    path('posts/', views.PostList.as_view(), name='post_list'),
    path('posts/<int:pk>/', views.PostDetail.as_view(), name='post_detail'),
    path('questions/', views.QuestionList.as_view(), name='question_list'),
]
