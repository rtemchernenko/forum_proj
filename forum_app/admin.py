from django.contrib import admin

from .models import Forum, Thread, Post, UserProfile
# Register your models here.

@admin.register(Forum)
class ForumAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = ('title', 'forum', 'started_by', 'created_at')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('content', 'thread', 'created_by', 'created_at')
    prepopulated_fields = {'slug': ('content',)}

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'avatar', 'signature', 'post_count')
