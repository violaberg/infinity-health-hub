from django import forms
from django_summernote.widgets import SummernoteWidget
from .models import Reply, Post, Article


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['body']


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'content', 'image']


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content', 'image']
        widgets = {
            'title': SummernoteWidget(),
            'content': SummernoteWidget(),
        }
