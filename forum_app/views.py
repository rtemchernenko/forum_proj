from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView, CreateView, UpdateView, FormMixin, DeleteView
from .forms import RegisterForm, CommentForm, AvatarUploadForm, CreatePostForm
from .models import Forum, Thread, Post, UserProfile, Comment
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.utils.text import slugify
import uuid
from django.shortcuts import redirect
from django.urls import reverse


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
            return redirect(reverse('forum_app:post_detail', kwargs={'forum_slug': post.thread.forum.slug,
                                                                     'thread_slug': post.thread.slug,
                                                                     'slug': post.slug}))

        context = self.get_context_data()
        context['comment_form'] = comment_form
        return self.render_to_response(context)


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment

    def test_func(self):
        # Эта функция будет вызвана, чтобы проверить, имеет ли пользователь право на удаление комментария
        comment = self.get_object()
        return self.request.user == comment.created_by

    def get_success_url(self):
        # Возвращаем URL, куда перейти после успешного удаления комментария
        comment = self.get_object()
        return reverse('forum_app:post_detail', kwargs={
            'forum_slug': comment.post.thread.forum.slug,
            'thread_slug': comment.post.thread.slug,
            'slug': comment.post.slug
        })


# Регистрация
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
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user=request.user)

        if request.method == 'POST':
            form = AvatarUploadForm(request.POST, request.FILES)
            if form.is_valid():
                user_profile.avatar = form.cleaned_data['avatar']
                user_profile.save()
                return redirect('/profile')  # Перенаправление на страницу профиля после загрузки
        else:
            form = AvatarUploadForm()

        return render(request, 'forum_app/profile.html', {'form': form, 'user_profile': user_profile})
    else:
        return redirect('login')


class CreatePostView(FormView):
    form_class = CreatePostForm
    template_name = 'forum_app/creation-post.html'

    def form_valid(self, form):
        new_post = form.save(commit=False)
        unique_slug = f"{slugify(new_post.title)}-{str(uuid.uuid4())[:8]}"
        new_post.slug = unique_slug
        new_post.created_by = self.request.user
        new_post.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('forum_app:create-post')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['threads'] = Thread.objects.all()
        return context


class GetThreadsForForumView(View):
    def get(self, request, forum_id):
        threads = Thread.objects.filter(forum_id=forum_id).values('id', 'title')
        return JsonResponse(list(threads), safe=False)
