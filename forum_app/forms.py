from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import Textarea

from .models import Comment

from forum_app.models import UserProfile


class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content', ]
        labels = {
            'content': '',  # Пустая строка для уборки надписи
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

        # Добавляем параметр no-resize для отключения изменения размера
        self.fields['content'].widget = Textarea(attrs={'rows': 10, 'cols': 35, 'style': 'resize: none;'})


class AvatarUploadForm(forms.Form):
    avatar = forms.ImageField()
