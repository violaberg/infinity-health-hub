from django.shortcuts import render, get_object_or_404
from forum.models import Article, Post

# Create your views here.


def index(request):
    articles = Article.objects.filter(is_approved=True)
    posts = Post.objects.filter(is_approved=True)

    return render(request, 'index.html', {'articles': articles, 'posts': posts})


def about(request):
    return render(request, 'about.html')


def resources(request):
    return render(request, 'resources.html')
