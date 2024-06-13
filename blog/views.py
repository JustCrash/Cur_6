from pytils.translit import slugify
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

from blog.models import Blog
from blog.utils import get_cache_mailing_active, get_mailing_count_from_cache, get_cache_unique_quantity


class BlogListView(ListView):
    model = Blog
    template_name = 'blog/blog_list.html'
    extra_context = {'title': 'Блог'}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mailing_quantity_active'] = get_cache_mailing_active()
        context['mailing_quantity'] = get_mailing_count_from_cache()
        context['clients_unique_quantity'] = get_cache_unique_quantity()
        context['records'] = Blog.objects.order_by('?')[:3]
        return context


class BlogCreateView(CreateView):
    model = Blog
    fields = ['title', 'content', 'preview', 'publication_sign', 'number_of_views']
    template_name = 'blog/blogpost_from.html'
    success_url = reverse_lazy('blog:blogpost_form')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавить запись в блог'
        return context

    def form_valid(self, form):
        if form.is_valid():
            new_blog = form.save()
            new_blog.slug = slugify(new_blog.title)
            new_blog.save()
        return super().form_valid(form)