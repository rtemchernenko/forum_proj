from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.core.files import File
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic.base import TemplateView
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView, CreateView, UpdateView, FormMixin

from .forms import RegisterForm, CommentForm
from .models import Forum, Thread, Post, UserProfile, Comment
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
    template_name = 'forum_app/posts.html'
    context_object_name = 'posts'

    def get_queryset(self):
        self.thread = get_object_or_404(Thread, slug=self.kwargs['thread_slug'])
        return Post.objects.filter(thread=self.thread)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['thread'] = self.thread
        return context


class PostDetailView(DetailView):
    model = Post
    slug_field = 'slug'
    template_name = 'forum_app/post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        context['comments'] = Comment.objects.filter(post=self.object)
        return context


# class PostDetailView(DetailView, FormMixin):
#     model = Post
#     slug_field = 'slug'
#     template_name = 'forum_app/post.html'
#     context_object_name = 'post'
#     form_class = CommentForm
#
#     def get_success_url(self):
#         return reverse_lazy('post_detail', kwargs={'pk': self.get_object().id})
#
#     def post(self, request, *args, **kwargs):
#         form = self.get_form()
#         if form.is_valid():
#             return self.form_valid(form)
#         else:
#             return self.form_invalid(form)
#
#     def form_valid(self, form):
#         self.object = form.save(commit=False)
#         self.object.post = self.get_object()
#         self.object.created_by = self.request.user
#         self.object.save()
#         return super().form_valid(form)
#
# def get_queryset(self):
#     self.thread = get_object_or_404(Thread, slug=self.kwargs['thread_slug'])
#     return Post.objects.filter(thread=self.thread)
#
# def get_context_data(self, **kwargs):
#     context = super().get_context_data(**kwargs)
#     context['thread'] = self.thread
#     return context


# Регистрация


@login_required
def profile_view(request):
    user_profile = UserProfile.objects.get(user=request.user)
    return render(request, 'forum_app/profile.html', {'user_profile': user_profile})


class RegisterView(FormView):
    form_class = RegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy("profile")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
