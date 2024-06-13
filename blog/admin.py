from django.contrib import admin

from blog.models import Blog


@ admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'content', 'number_of_views', 'date_of_publication']
    list_filter = ['date_of_publication']
    search_fields = ['title', 'content']