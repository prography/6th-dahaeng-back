from django.urls import path
from . import views
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

urlpatterns = [
    path('', views.login_test, name='login_test'),
    path('login/', obtain_jwt_token, name='login'),
    path('refresh/', refresh_jwt_token, name='refresh'),
    path('signup/', views.CreateProfileView.as_view(), name='signup'),
]
