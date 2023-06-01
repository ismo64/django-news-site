from django import template
from news.models import Category, New
from django.db.models import Count
from django.db.models import Q
from django.core.cache import cache

register = template.Library()

# @register.simple_tag()
# def get_categories():
#     return Category.objects.annotate(num_news=Count('news', filter=Q(news__is_published=True)))

@register.simple_tag()
def get_categories():
    categories = cache.get('categories')
    if not categories:
        categories = Category.objects.annotate(num_news=Count('news', filter=Q(news__is_published=True)))
        cache.set('categories', categories, 60)
    return categories

