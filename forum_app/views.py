from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.core.files import File
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic.base import TemplateView
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView, CreateView, UpdateView, FormMixin, DeleteView

from .forms import RegisterForm, CommentForm, AvatarUploadForm
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


from django.shortcuts import redirect
from django.urls import reverse


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

    def post(self, request, *args, **kwargs):
        post = self.get_object()  # Получаем текущий объект Post

        # Обработка отправки комментария
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post  # Используем post вместо self.object
            comment.created_by = request.user
            comment.save()

            # Перенаправление на ту же страницу с постом после добавления комментария
            return redirect(reverse('post_detail', kwargs={'forum_slug': post.thread.forum.slug,
                                                           'thread_slug': post.thread.slug,
                                                           'slug': post.slug}))  # Используем post вместо self.object

        # Если форма не прошла валидацию, обновите контекст с формой и комментариями
        context = self.get_context_data()
        context['comment_form'] = comment_form
        return self.render_to_response(context)


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment

    def get_success_url(self):
        comment = self.get_object()
        return reverse('post_detail', kwargs={
            'forum_slug': comment.post.thread.forum.slug,
            'thread_slug': comment.post.thread.slug,
            'slug': comment.post.slug
        })


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


def signature(request):
    user_profile = UserProfile.objects.get(user=request.user)
    context = {
        'user_profile': user_profile
    }

    return render(request, 'forum_app/profile.html', context)


def profile_view(request):
    user_profile = UserProfile.objects.get(user=request.user)

    if request.method == 'POST':
        form = AvatarUploadForm(request.POST, request.FILES)
        if form.is_valid():
            user_profile.avatar = form.cleaned_data['avatar']
            user_profile.save()
            return redirect('profile')  # Перенаправление на страницу профиля после загрузки
    else:
        form = AvatarUploadForm()

    return render(request, 'forum_app/profile.html', {'form': form, 'user_profile': user_profile})
