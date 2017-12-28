from django.contrib import admin
from .models import BlogArticles
# Register your models here.

class BlogArticlesAdmin(admin.ModelAdmin):
    ''' 定制admin '''
    list_display = ('id', 'title', 'author', 'publish',)
    list_filter = ('publish', 'author',)
    search_fields = ('title', 'body',)
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ('id',)
    list_per_page = 2
admin.site.register(BlogArticles, BlogArticlesAdmin)