from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name="main"),
    path('signup/', views.CreateProfileView.as_view(), name='signup'),
]
