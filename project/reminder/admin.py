from django.contrib import admin
from .models import Reminder


@admin.register(Reminder)
class RemainerAdmin(admin.ModelAdmin):
    pass
