from .models import New, Category
from django.db.models import Count

class DataMixin:
    paginate_by = 2
    
    def get_user_context(self, **kwargs):
        context = kwargs
        if context.get('cat_selected') is None:
            context['cat_selected'] = 0
        context['categories'] = Category.objects.annotate(num_news=Count('news')).filter(num_news__gt=0)
        return context


        
        