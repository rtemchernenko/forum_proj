from django.db import models
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.dispatch import receiver

# Create your models here.
from django.contrib.auth.models import User  # Для использования внутренней модели пользователя Django


class Forum(models.Model):
    title = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    def __str__(self):
        return self.title


class Thread(models.Model):
    title = models.CharField(max_length=200)
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE)
    started_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    def __str__(self):
        return self.title


class Post(models.Model):
    content = models.TextField()
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    def __str__(self):
        return f"Post by {self.created_by.username} in {self.thread.title}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    signature = models.CharField(max_length=200, blank=True)
    post_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.user.username if self.user else ""


def generate_slug(instance, source_field):
    return slugify(getattr(instance, source_field))


@receiver(pre_save, sender=Forum)
def create_slug(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = generate_slug(instance)

@receiver(pre_save, sender=Thread)
def create_thread_slug(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = generate_slug(instance, 'title')


@receiver(pre_save, sender=Post)
def create_post_slug(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = generate_slug(instance, 'content')[:50]