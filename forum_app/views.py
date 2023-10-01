from django.shortcuts import render
from django.core.files import File
from django.utils import timezone
from django.views.generic.base import TemplateView
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView, CreateView, UpdateView
from .models import Forum, Thread, Post, UserProfile
from django.http import HttpResponse
from django.views import View


# Create your views here.

class ForumListView(ListView):
    model = Forum
    template_name = 'forum_app/forum.html'  # замените 'your_template_name.html' на имя вашего шаблона
    context_object_name = 'forums'  # используйте 'forums' для доступа к списку форумов в вашем шаблоне


class ThreadListView(ListView):
    model = Thread
    template_name = 'forum_app/thread.html'
    context_object_name = 'threads'


class PostListView(ListView):
    model = Post
    template_name = 'forum_app/post.html'
    context_object_name = 'posts'
