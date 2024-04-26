from django.db import models
from django.contrib.auth.models import User
from profiles.models import NeuroDiversity, LifeStage


class Article(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    content = models.TextField()
    image = models.ImageField(
        upload_to='article_images/', null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    is_approved = models.BooleanField(default=False)
    life_stage = models.ManyToManyField(LifeStage)
    neurodiversity = models.ManyToManyField(NeuroDiversity)
    likes = models.ManyToManyField(
        User, related_name='liked_articles', blank=True)
    saved_by = models.ManyToManyField(
        User, related_name='saved_articles', blank=True)

    def __str__(self):
        return self.title

    @property
    def likes_count(self):
        return self.likes.count()


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to='post_images/', null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    is_approved = models.BooleanField(default=False)
    life_stage = models.ManyToManyField(LifeStage)
    neurodiversity = models.ManyToManyField(NeuroDiversity)
    likes = models.ManyToManyField(
        User, related_name='liked_posts', blank=True)
    saved_by = models.ManyToManyField(
        User, related_name='saved_posts', blank=True)

    def __str__(self):
        return self.title

    @property
    def likes_count(self):
        return self.likes.count()

    @property
    def replies_count(self):
        return self.replies.filter(approved=True).count()


class Reply(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='replies')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_on']
        verbose_name_plural = 'replies'

    def __str__(self):
        return f"(Reply {self.body} by {self.author}"
