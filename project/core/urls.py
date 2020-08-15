"""
TODO: 내가 바꾼 URL 명시 하기
'jorang_create/' -> 'jorang/'


로그인 및 JWT
1. signup -> 회원 가입
2. login -> JWT Token 얻기
2.5 login_test -> 로그인 되었나 확인하기.
3. refresh -> JWT token refresh 하기, 즉 새로 얻기
--------------------------------

TODO: 메일 부분 좀더 공부하고 더 간단하게 짜자.
메일 처리하기
1. user_active

--------------------------------
조랭이 만들기
1. jorang/


--------------------------------

profile Detail
1. profile/<int:profile_id>/ -> GET profile_id 에 해당하는 Profile 의 세부정보를 넘겨준다.
2. profile/<int:profile_id>/ -> POST profile_id 에 해당하는 Profile 의 조랭이의 세부정보를 만든다.


--------------------------------
# TODO: attendance 이거 언제 작동하는 거지? 언제 사용이 되는 지 확인을 해야겠다.
1. attendance

--------------------------------
# TODO : 이거 어떻게 하는지 거의 모르겠다.
# SOCIAL LOGIN



"""
from django.urls import path
from .API import login
from .API import jorang
from .API import profile
from .API import attendance
from rest_framework_jwt.views import refresh_jwt_token

urlpatterns = [
    # login 및 JWT Token
    path('', login.login_test, name='login_test'),
    path('signup/', login.CreateProfileView.as_view(), name='signup'),
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
