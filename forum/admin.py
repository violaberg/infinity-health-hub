from django.contrib import admin
from .models import Article, Post, Reply
from django_summernote.admin import SummernoteModelAdmin


class ArticleAdmin(SummernoteModelAdmin):
    list_display = ('title', 'author', 'created_on', 'is_approved')
    list_filter = ('is_approved', 'life_stage', 'neurodiversity')
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    summernote_fields = ('content')

class PostAdmin(SummernoteModelAdmin):
    list_display = ('title', 'author', 'created_on', 'is_approved')
    list_filter = ('is_approved',)
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    summernote_fields = ('content')

class ReplyAdmin(admin.ModelAdmin):
    list_display = ('author', 'body')

admin.site.register(Article, ArticleAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Reply, ReplyAdmin)
