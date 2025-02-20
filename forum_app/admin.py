from django.contrib import admin
from django.apps import apps
from .models import Forum, Thread, Post, UserProfile, Comment

# Register your models here.

app = apps.get_app_config('graphql_auth')

for model_name, model in app.models.items():
    admin.site.register(model)


@admin.register(Forum)
class ForumAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = ('title', 'forum', 'started_by', 'created_at')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('forum',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'thread', 'created_by', 'created_at')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('thread', 'created_by',)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'email', 'avatar', 'signature', 'post_count')
    list_editable = ('signature', 'email')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('content', 'post', 'created_by', 'created_at')
    search_fields = ('content', 'post__title', 'created_by__username')
    list_filter = ('created_at',)
