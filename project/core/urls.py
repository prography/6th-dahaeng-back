"""
로그인 및 JWT
1. signup -> 회원 가입
2. login -> JWT Token 얻기
2.5 login_test -> 로그인 되었나 확인하기.
3. refresh -> JWT token refresh 하기, 즉 새로 얻기

--------------------------------
메일 처리하기
1. user_active -> 메일로 보낸 profile_id64 와 token 을 받아서 user 를 active 하게 만듬.

--------------------------------
조랭이 만들기
1. jorang/

--------------------------------
profile Detail
1. profile/<int:profile_id>/ -> GET profile_id 에 해당하는 Profile 의 세부정보를 넘겨준다.
2. profile/<int:profile_id>/ -> POST profile_id 에 해당하는 Profile 의 조랭이의 세부정보를 만든다.

--------------------------------
1. attendance/ -> GET


--------------------------------
# TODO : 이거 어떻게 하는지 거의 모르겠다. 앞으로, 이부붑을 좀 더 공부해서, 기능을 구현을 할 수 있어야 한다.
# SOCIAL LOGIN



"""
from rest_framework_jwt.views import refresh_jwt_token
from django.urls import path
from .API import login
from .API import jorang
from .API import profile
from .API import attendance


urlpatterns = [
    # login 및 JWT Token
    path('', login.login_test, name='login_test'),
    path('signup/', login.CreateProfileView.as_view(), name='signup'),
    path('user_active/', login.user_active, name='user_active'),
    path('login/', login.MyObtainJSONWebToken.as_view(), name='login'),
    path('refresh/', refresh_jwt_token, name='refresh'),

    # 조랭이 만들기
    path('jorang/', jorang.create, name='jorang_create'),

    # Profile Detail 조랭이
    path('profile/<int:profile_id>/', profile.ProfileDetailView.as_view(), name="profile"),

    # 출석 체크
    path('attendance/', attendance.AttendanceView.as_view(), name='attendance'),

    # 이부분은 나중에, social login 을 정리를 하고 난뒤에 보는 것이 맞겠다.
    # path('social/', include(router.urls)),

]
