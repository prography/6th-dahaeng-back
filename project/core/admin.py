from django.contrib import admin
from .models import Profile, Jorang, UserCoin


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'last_login']


@admin.register(Jorang)
class ProfileAdmin(admin.ModelAdmin):
    pass

@admin.register(UserCoin)
class UserCoinAdmin(admin.ModelAdmin):
    list_display = ['profile', 'last_date', 'coin']
