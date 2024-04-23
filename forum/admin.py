from django.contrib import admin
from .models import Article, Post

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_on', 'is_approved')
    list_filter = ('is_approved', 'life_stage', 'neurodiversity')
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_on', 'is_approved')
    list_filter = ('is_approved',)
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Article, ArticleAdmin)
admin.site.register(Post, PostAdmin)
