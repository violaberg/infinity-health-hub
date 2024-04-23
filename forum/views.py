from django.shortcuts import render, get_object_or_404
from .models import Article, Post


def forum(request):
     
    return render(request, 'forum/forum.html')


def article_list(request):
    articles = Article.objects.filter(is_approved=True)
    return render(request, 'forum/article_list.html', {'articles': articles})

def post_list(request):
    posts = Post.objects.filter(is_approved=True)
    return render(request, 'forum/post_list.html', {'posts': posts})

def article_detail(request, slug):
    article = get_object_or_404(Article, slug=slug)
    return render(request, 'forum/article_detail.html', {'article': article})

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    return render(request, 'forum/post_detail.html', {'post': post})