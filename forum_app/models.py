from django.db import models
from django.utils.text import slugify
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils import timezone
import datetime
from django.contrib.auth.models import User


# Create your models here.


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
    created_at = models.DateTimeField(default=timezone.now)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    def __str__(self):
        return self.title


class Post(models.Model):
    title = models.TextField(max_length=200)
    content = models.TextField()
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    def __str__(self):
        return f"Post by {self.created_by.username} in {self.thread.title}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', blank=True, default='avatars/avatar13.jpg')
    signature = models.CharField(max_length=200, blank=True)
    post_count = models.PositiveIntegerField(default=0)

    def increment_post_count(self):
        self.post_count += 1
        self.save()

    def __str__(self):
        return self.user.username if self.user else ""


class Comment(models.Model):
    content = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Comment by {self.created_by.username} on {self.post.slug}"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=Post)
def increment_post_count(sender, instance, created, **kwargs):
    if created:
        profile = UserProfile.objects.get(user=instance.created_by)
        profile.increment_post_count()


def generate_slug(instance, source_field):
    return slugify(getattr(instance, source_field))


@receiver(pre_save, sender=Forum)
def create_slug(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = generate_slug(instance, 'title')


@receiver(pre_save, sender=Thread)
def create_thread_slug(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = generate_slug(instance, 'title')


@receiver(pre_save, sender=Post)
def create_post_slug(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = generate_slug(instance, 'title')[:50]
