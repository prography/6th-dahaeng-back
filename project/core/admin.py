from django.contrib import admin
from .models import Profile, Jorang, UserCoin, Attendance, PushNotificationMessage, UserFeedback


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'last_login', 'social']


@admin.register(Jorang)
class JorangAdmin(admin.ModelAdmin):
    pass


@admin.register(UserCoin)
class UserCoinAdmin(admin.ModelAdmin):
    list_display = ['profile', 'last_date', 'coin']


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    pass

@admin.register(PushNotificationMessage)
class PushNotificationMessageAdmin(admin.ModelAdmin):
    pass

@admin.register(UserFeedback)
class UserFeedbackAdmin(admin.ModelAdmin):
    pass
