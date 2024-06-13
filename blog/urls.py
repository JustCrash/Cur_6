from django.urls import path
from django.views.decorators.cache import cache_page

from blog.views import BlogListView, BlogCreateView

from blog.apps import BlogConfig

app_name = BlogConfig.name

urlpatterns = [
    path('', BlogListView.as_view(), name='blog_list'),
]