from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Article, Post
from .forms import ReplyForm


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

def post_detail(request, post_id):
    queryset = Post.objects.all()
    post = get_object_or_404(queryset, pk=post_id)
    reply = post.replies.filter(approved=True).order_by('created_on')
    liked = False
    saved = False

    if request.user.is_authenticated and post.likes.filter(id = request.user.id).exists():
        liked = True

    if request.user.is_authenticated and post.saved_by.filter(id = request.user.id).exists():
        saved = True
    
    if request.method == 'POST':
        reply_form = ReplyForm(data=request.POST)
        if reply_form.is_valid():
            reply_form.instance.author = request.user
            reply = reply_form.save(commit=False)
            reply.post = post
            reply.save()
            messages.success(request, 'Reply submitted! Please wait for approval.')
            return redirect('post_detail', post_id=post_id)
        else:
            reply_form = ReplyForm()
            messages.error(request,
                           'Update failed. Please ensure the form is valid.')
    else:
        reply_form = ReplyForm()
    
    context = {
        'post': post,
        'reply': reply,
        'reply_form': reply_form,
        'replied': request.method == 'POST',
        'liked': liked,
        'saved': saved,
        'post_id': post_id
    }
    return render(request, 'forum/post_detail.html', context)