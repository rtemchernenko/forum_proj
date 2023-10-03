from django.contrib import admin
from django.urls import path
from . import views
from .views import ForumListView, ThreadListView, PostListView, profile_view

urlpatterns = [
    path('forums/', ForumListView.as_view(), name='forum_list'),
    path('forums/<slug:forum_slug>/', ThreadListView.as_view(), name='thread_list'),
    path('forums/<slug:forum_slug>/<slug:thread_slug>/', PostListView.as_view(), name='post_list'),
    path('profile', profile_view, name='profile'),

]
