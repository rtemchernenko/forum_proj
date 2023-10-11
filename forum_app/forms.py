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

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     for field in self.fields:
    #         self.fields[field].widget.attrs['class'] = 'form-control'
    #     self.fields['content'].widget = Textarea(attrs={'rows': 5})
