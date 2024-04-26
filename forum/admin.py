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
    # Add 'life_stage' and 'neurodiversity' to list_filter
    list_filter = ('is_approved', 'life_stage', 'neurodiversity')
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    summernote_fields = ('content')

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj:
            form.base_fields['is_approved'].initial = True
            # Pre-select 'life_stage' field
            form.base_fields['life_stage'].initial = obj.life_stage
            # Pre-select 'neurodiversity' field
            form.base_fields['neurodiversity'].initial = obj.neurodiversity
        return form


class ReplyAdmin(admin.ModelAdmin):
    list_display = ('author', 'body')


admin.site.register(Article, ArticleAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Reply, ReplyAdmin)
