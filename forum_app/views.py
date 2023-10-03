from django.shortcuts import render, get_object_or_404
from django.core.files import File
from django.utils import timezone
from django.views.generic.base import TemplateView
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView, CreateView, UpdateView
from .models import Forum, Thread, Post, UserProfile
from django.http import HttpResponse
from django.views import View


# Create your views here.

# Отображение контента
class ForumListView(ListView):
    model = Forum
    template_name = 'forum_app/forum.html'  # Подменяем имя шаблона, если по умолчанию не подходит
    context_object_name = 'forums'


class ThreadListView(ListView):
    model = Thread
    template_name = 'forum_app/thread.html'
    context_object_name = 'threads'

    def get_queryset(self):
        self.forum = get_object_or_404(Forum, slug=self.kwargs['forum_slug'])
        return Thread.objects.filter(forum=self.forum)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['forum'] = self.forum
        return context


class PostListView(ListView):
    model = Post
    template_name = 'forum_app/post.html'
    context_object_name = 'posts'

    def get_queryset(self):
        self.thread = get_object_or_404(Thread, slug=self.kwargs['thread_slug'])
        return Post.objects.filter(thread=self.thread)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['thread'] = self.thread
        return context

    # Регистрация


def profile_view(request):
    return render(request, 'forum_app/profile.html')
