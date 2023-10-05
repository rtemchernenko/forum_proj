from django.contrib import admin
from django.urls import path
from . import views
from .views import ForumListView, ThreadListView, PostDetailView, profile_view, RegisterView, PostListView
from django.conf import settings
from django.conf.urls.static import static

# app_name = 'forum_app'

urlpatterns = [
    path('forums/', ForumListView.as_view(), name='forum_list'),
    path('forums/<slug:forum_slug>/threads/', ThreadListView.as_view(), name='thread_list'),
    path('forums/<slug:forum_slug>/threads/<slug:thread_slug>/posts/', PostListView.as_view(), name='post_list'),
    path('forums/<slug:forum_slug>/threads/<slug:thread_slug>/posts/<slug:slug>/', PostDetailView.as_view(), name='post_detail'),
    path('profile', profile_view, name='profile'),
    path('register', RegisterView.as_view(), name='register'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
