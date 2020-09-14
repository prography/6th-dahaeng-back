"""
     # TODO: 아직 현재에는 무었이 무었인지 모르겠다.
     나중에 전체적으로 코드를 정리를 하고 난 뒤에 보는 것이 맞겠다.
"""
#
# from django.contrib.auth.models import update_last_login
# from django.contrib.auth import get_user_model
# from django.shortcuts import redirect
# from core.serializers import ProfileSerializer, UserCoinSerializer
# from core.models import Profile, Jorang
# from core.social_login.kakao_social_login import KakaoSocialLogin
# from record.serializers import UserQuestionSerializer
# from record.models import UserQuestion
# from rest_framework_jwt.settings import api_settings
# from rest_framework import permissions, status, viewsets, permissions
# from rest_framework.response import Response
# from rest_framework.decorators import action, api_view, authentication_classes, permission_classes
# import requests
# from uuid import uuid4
# import json
# from datetime import date
# from core.social_login.naver_social_login import NaverSocialLogin
#
#
# class UserSocialViewSet(viewsets.ModelViewSet):
#     queryset = Profile.objects.all()
#     serializer_class = ProfileSerializer
#     permission_classes = [permissions.AllowAny]
#     state_token_code = uuid4().hex
#
#     def __init__(self, **kwargs):
#         self.kakao_social_login = KakaoSocialLogin()
#         self.naver_social_login = NaverSocialLogin(self.state_token_code)
#         super(UserSocialViewSet, self).__init__(**kwargs)
#
#     @action(detail=False, methods=['get'], url_path='kakao_login')
#     def get_kakao_auth_token(self, request, pk=None):
#         url = self.kakao_social_login.get_auth_url()
#         return redirect(url)
#
#     @action(detail=False, methods=['get'], url_path='kakao_login_callback')
#     def kakao_login_callback(self, request, pk=None):
#         try:
#             user_data_per_field = self.kakao_social_login.get_user_data(
#                 request)
#         except Exception as e:
#             return self.error_with_message(e)
#
#         if self._have_already_sign_up_for_other_social(user_data_per_field):
#             what_social_did_user_already_sign_up = Profile.objects.get(
#                 email=user_data_per_field['email']).social
#             return Response({
#                 'message': f'이미 {what_social_did_user_already_sign_up}로 가입했습니다. {what_social_did_user_already_sign_up}로 로그인 해주세요.'
#             }, status=status.HTTP_400_BAD_REQUEST)
#
#         if Profile.objects.filter(email=user_data_per_field['email'], social=user_data_per_field['social']):
#             user = self.kakao_social_login.login(user_data_per_field)
#         else:
#             user = self.kakao_social_login.sign_up(user_data_per_field)
#
#         is_first_login = False
#         User = get_user_model()
#         email = user.email
#         try:
#             profile = User.objects.get(email=email)
#         except User.DoesNotExist:
#             return Response({
#                 'response': 'error',
#                 'message': '유효하지않은 계정입니다.'
#             })
#
#         if profile.last_login is None:
#             is_first_login = True
#             serializer = UserQuestionSerializer(
#                 data={"profile": email}, partial=True)
#             if serializer.is_valid():
#                 serializer.save()
#             usercoinSerializer = UserCoinSerializer(data={"profile": email})
#             if usercoinSerializer.is_valid():
#                 usercoinSerializer.save()
#
#         else:
#             userq = UserQuestion.objects.get(profile=profile.id)
#             serializer = UserQuestionSerializer(
#                 userq, data={"last_login": date.today()}, partial=True)
#             if serializer.is_valid():
#                 serializer.save()
#
#         try:
#             jorang = Jorang.objects.get(profile=profile)
#             has_jorang = True
#             jorang_nickname = jorang.nickname
#             jorang_color = jorang.color
#         except Jorang.DoesNotExist:
#             has_jorang = False
#             jorang_nickname = None
#             jorang_color = None
#
#         update_last_login(None, profile)
#
#         jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
#         jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
#
#         payload = jwt_payload_handler(user)
#         token = jwt_encode_handler(payload)
#
#         return Response({
#             'response': 'success',
#             'message': {
#                 'token': token,
#                 'profile_id': profile.id,
#                 'has_jorang': has_jorang,
#                 'jorang': {
#                         'nickname': jorang_nickname,
#                         'color': jorang_color
#                 }
#             }
#         })
#
#     def error_with_message(self, e):
#         if e.args:
#             detail = e.args[0]
#             error_name = e.__class__.__name__
#         return Response({"message": f'{error_name}가 발생했습니다. {detail}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#
#     def _have_already_sign_up_for_other_social(self, user_data_per_field):
#         user = Profile.objects.filter(email=user_data_per_field['email'])
#         if user.count() > 1:
#             raise AssertionError('해당 이메일로 가입된 계정이 이미 존재합니다. 관리자에게 문의해주세요.')
#         if user.count() == 1:
#             user = user[0]
#             return user.social != user_data_per_field['social']
#         return False
#
#     @action(detail=False, methods=['get'], url_path='naver_login')
#     def get_naver_auth_token(self, request, pk=None):
#         url = self.naver_social_login.get_auth_url()
#         return redirect(url)
#
#     @action(detail=False, methods=['get'], url_path='naver_login_callback')
#     def naver_login_callback(self, request, pk=None):
#         callback_status_token_code = request.query_params.get('state')
#         if callback_status_token_code != self.naver_social_login.state_token_code:
#             return Response({'message': 'state token code is not valid'}, status=status.HTTP_401_UNAUTHORIZED)
#
#         try:
#             user_data_per_field = self.naver_social_login.get_user_data(
#                 request)
#         except Exception as e:
#             return self.error_with_message(e)
#
#         if self._have_already_sign_up_for_other_social(user_data_per_field):
#             what_social_did_user_already_sign_up = User.objects.get(
#                 email=user_data_per_field['email']).social
#             return Response({
#                 'message': f'이미 {what_social_did_user_already_sign_up}로 가입했습니다. {what_social_did_user_already_sign_up}로 로그인 해주세요.'
#             }, status=status.HTTP_400_BAD_REQUEST)
#
#         User = get_user_model()
#         if User.objects.filter(email=user_data_per_field['email'], social=user_data_per_field['social']):
#             user = self.naver_social_login.login(user_data_per_field)
#         else:
#             user = self.naver_social_login.sign_up(user_data_per_field)
#
#         is_first_login = False
#         User = get_user_model()
#         email = user.email
#         try:
#             profile = User.objects.get(email=email)
#         except User.DoesNotExist:
#             return Response({
#                 'response': 'error',
#                 'message': '유효하지않은 계정입니다.'
#             })
#
#         if profile.last_login is None:
#             is_first_login = True
#             serializer = UserQuestionSerializer(
#                 data={"profile": email}, partial=True)
#             if serializer.is_valid():
#                 serializer.save()
#             usercoinSerializer = UserCoinSerializer(data={"profile": email})
#             if usercoinSerializer.is_valid():
#                 usercoinSerializer.save()
#
#         else:
#             userq = UserQuestion.objects.get(profile=profile.id)
#             serializer = UserQuestionSerializer(
#                 userq, data={"last_login": date.today()}, partial=True)
#             if serializer.is_valid():
#                 serializer.save()
#
#         try:
#             jorang = Jorang.objects.get(profile=profile)
#             has_jorang = True
#             jorang_nickname = jorang.nickname
#             jorang_color = jorang.color
#         except Jorang.DoesNotExist:
#             has_jorang = False
#             jorang_nickname = None
#             jorang_color = None
#
#         update_last_login(None, profile)
#
#         jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
#         jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
#
#         payload = jwt_payload_handler(user)
#         token = jwt_encode_handler(payload)
#
#         return Response({
#             'response': 'success',
#             'message': {
#                 'token': token,
#                 'profile_id': profile.id,
#                 'has_jorang': has_jorang,
#                 'jorang': {
#                         'nickname': jorang_nickname,
#                         'color': jorang_color
#                 }
#             }
#         })
#
#     def _naver_login_or_sign_up(self, dahaeng_user_data):
#         # 사용 안함
#         User = get_user_model()
#         email = dahaeng_user_data['email']
#         social = dahaeng_user_data['social']
#         user = User.objects.filter(email=email)
#
#         if user.exists():
#             user = User.objects.get(email=email)
#             if user.social == social:
#                 user = naver.login(dahaeng_user_data)
#                 return user
#             else:
#                 already_signup_social = user.social
#                 if already_signup_social == 'NONE':
#                     already_signup_social = "눈송이"
#                 return already_signup_social
#
#         user = naver.sign_up(dahaeng_user_data)
#         return user
#

# https://kauth.kakao.com/oauth/authorize?client_id={app_key}&redirect_uri={redirect_uri}&response_type=code
# https://kauth.kakao.com/oauth/authorize?client_id=ea0c660893539d787993dada9b5ccba2&redirect_uri=http://localhost:8000/social/kakao_login_callback/&response_type=code
