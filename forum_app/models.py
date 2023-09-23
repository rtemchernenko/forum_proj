from django.db import models

# Create your models here.
from django.contrib.auth.models import User  # Для использования внутренней модели пользователя Django

class Forum(models.Model):
    title = models.CharField(max_length=200, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.title

class Thread(models.Model):
    title = models.CharField(max_length=200)
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE)
    started_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Post(models.Model):
    content = models.TextField()
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Post by {self.created_by.username} in {self.thread.title}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    signature = models.CharField(max_length=200, blank=True)
    post_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.user.username