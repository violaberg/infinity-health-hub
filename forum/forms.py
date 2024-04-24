from django import forms
from .models import Reply, Post


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['body']


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'content', 'image']
