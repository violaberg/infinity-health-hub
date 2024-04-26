from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Article, Post
from .forms import ReplyForm
from .forms import PostForm, ArticleForm
from django.utils.text import slugify


def is_admin(user):
    return user.is_superuser


@login_required
def post_list(request):
    user = request.user
    # Get the saved filter from the query parameters
    saved_filter = request.GET.get('saved_posts')

    if user.is_authenticated:
        user_profile = request.user.userprofile
        life_stages = user_profile.lifestage.all()
        neurodiversities = user_profile.neurodiversity.all()
        is_approved = user_profile.is_approved
        saved_posts = user.saved_posts.all()

        if saved_filter == 'true':
            # Filter posts to show only saved posts
            posts = saved_posts.filter(
                life_stage__in=life_stages,
                neurodiversity__in=neurodiversities,
                is_approved=True
            ).distinct()
        elif saved_filter == 'false':
            # Filter posts to show only posts that are not saved
            posts = Post.objects.filter(
                life_stage__in=life_stages,
                neurodiversity__in=neurodiversities,
                is_approved=True
            ).exclude(id__in=saved_posts).distinct()
        else:
            # Show all posts
            posts = Post.objects.filter(
                life_stage__in=life_stages,
                neurodiversity__in=neurodiversities,
                is_approved=True
            ).distinct()

        context = {
            'posts': posts,
            'is_approved': is_approved,
            'saved_posts': saved_posts
        }

        return render(request, 'forum/post_list.html', context)

    return render(request, 'forum/post_list.html')


@login_required
def create_post(request):
    if request.method == 'POST':
        post_form = PostForm(data=request.POST)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.author = request.user
            post.slug = slugify(post.title)
            post.save()

            # Now that the post instance is saved, we can set the many-to-many relationships
            post.life_stage.set(request.user.userprofile.lifestage.all())
            post.neurodiversity.set(
                request.user.userprofile.neurodiversity.all())

            messages.success(request, 'Post created successfully!')
            return redirect('post_detail', post_id=post.id)
        else:
            messages.error(
                request, 'Failed to create post. Please ensure the form is valid.')
    else:
        post_form = PostForm()

    context = {
        'post_form': post_form,
    }
    return render(request, 'forum/create_post.html', context)


@login_required
def post_detail(request, post_id):
    queryset = Post.objects.all()
    post = get_object_or_404(queryset, pk=post_id)
    reply = post.replies.filter(approved=True).order_by('created_on')
    liked = False
    saved = False

    if request.user.is_authenticated and post.likes.filter(id=request.user.id).exists():
        liked = True

    if request.user.is_authenticated and post.saved_by.filter(id=request.user.id).exists():
        saved = True

    if request.method == 'POST':
        reply_form = ReplyForm(data=request.POST)
        if reply_form.is_valid():
            reply_form.instance.author = request.user
            reply = reply_form.save(commit=False)
            reply.post = post
            reply.save()
            messages.success(
                request, 'Reply submitted! Please wait for approval.')
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


@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    if post.author != request.user:
        return render(request, 'forum/unauthorised_access.html')

    if request.method == 'POST':
        post_form = PostForm(data=request.POST, instance=post)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.is_approved = False  # Set the post to not approved
            post.save()
            messages.success(
                request, 'Post updated successfully! Please wait for approval.')
            # return redirect('post_detail', post_id=post.id)
            return redirect('posts')
        else:
            messages.error(
                request, 'Failed to update post. Please ensure the form is valid.')
    else:
        post_form = PostForm(instance=post)

    context = {
        'post_form': post_form,
        'post_id': post_id,
        'post': post
    }
    return render(request, 'forum/edit_post.html', context)


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    if post.author != request.user:
        return render(request, 'forum/unauthorised_access.html')

    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted successfully!')
        return redirect('posts')

    context = {
        'post': post,
        'post_id': post_id
    }
    return render(request, 'forum/delete_post.html', context)


@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect('post_detail', post_id=post_id)


@login_required
def save_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if post.saved_by.filter(id=request.user.id).exists():
        post.saved_by.remove(request.user)
        messages.success(request, 'Post removed from saved posts.')
    else:
        post.saved_by.add(request.user)
        messages.success(request, 'Post saved successfully.')
    return redirect('post_detail', post_id=post_id)


def article_list(request):
    articles = Article.objects.filter(is_approved=True)
    return render(request, 'forum/article_list.html', {'articles': articles})


def article_detail(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    return render(request, 'forum/article_detail.html', {'article': article})


@user_passes_test(is_admin)
def create_article(request):

    if not request.user.is_superuser:
        return render(request, 'forum/unauthorised_access.html')

    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.slug = slugify(article.title)
            article.save()
            messages.success(
                request, 'Article created successfully! Please wait for approval.')
            return redirect('article_detail', article_id=article.id)
    else:
        form = ArticleForm()
    return render(request, 'forum/create_article.html', {'form': form})


@user_passes_test(is_admin)
def update_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)

    if not request.user.is_superuser:
        return render(request, 'forum/unauthorised_access.html')

    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form = form.save(commit=False)
            article.is_approved = False
            form.save()
            messages.success(
                request, 'Article updated successfully! Please wait for approval.')
            return redirect('article_detail', article_id=article.id)
    else:
        form = ArticleForm(instance=article)
    return render(request, 'forum/update_article.html', {'form': form, 'article': article})


@user_passes_test(is_admin)
def delete_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)

    if not request.user.is_superuser:
        return render(request, 'forum/unauthorised_access.html')

    if request.method == 'POST':
        article.delete()
        messages.success(request, 'Article deleted successfully!')
        return redirect('resources')
    return render(request, 'forum/delete_article.html', {'article': article, 'article_id': article_id})
