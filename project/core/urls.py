from django.urls import path
from . import views
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

urlpatterns = [
    path('', views.login_test, name='login_test'),
    path('login/', views.MyObtainJSONWebToken.as_view(), name='login'),
    path('refresh/', refresh_jwt_token, name='refresh'),
    path('signup/', views.CreateProfileView.as_view(), name='signup'),
    path('user_active/',
         views.user_active, name='user_active'),
    path('jorang_create/', views.jorang_create, name='jorang_create'),
    path('profile/<int:profile_id>/',
         views.ProfileDetailView.as_view(), name="profile"),
]
