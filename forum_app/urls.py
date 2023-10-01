from django.contrib import admin
from django.urls import path
from . import views
from .views import ForumListView, ThreadListView, PostListView

urlpatterns = [
    path('forums', ForumListView.as_view(), name='forums'),

    path('forums/<slug:forum_slug>', ThreadListView.as_view(), name='threads'),

    path('forums/<slug:forum_slug>/<slug:thread_slug>', PostListView.as_view(), name='post'),

]
