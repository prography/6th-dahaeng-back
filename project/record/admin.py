from django.contrib import admin
from .models import Post, Question, UserQuestion


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    pass


@admin.register(Question)
class PostAdmin(admin.ModelAdmin):
    pass

@admin.register(UserQuestion)
class PostAdmin(admin.ModelAdmin):
    pass
