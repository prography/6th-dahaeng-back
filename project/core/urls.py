from django.urls import path
from . import views
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

urlpatterns = [
    path('', views.login_test, name='login_test'),
    path('login/', obtain_jwt_token, name='login'),
    path('refresh/', refresh_jwt_token, name='refresh'),
    path('signup/', views.CreateProfileView.as_view(), name='signup'),
    path('send_email_for_active/', views.send_email_for_active,
         name='send_email_for_active'),
    path('user_active/',
         views.user_active, name="user_active"),
]
