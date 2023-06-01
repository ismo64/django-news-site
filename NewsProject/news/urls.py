from django.urls import path
from django.views.decorators.cache import cache_page
from .views import NewsHome, AddNews, ShowNews, ShowCategory, NewsCategory, register_user, LoginUser, logout_user

urlpatterns = [
    path('', NewsHome.as_view(), name='home'),
    path('cat/<int:cat_id>/', NewsCategory.as_view(), name='category'),
    path('news/add_news/', AddNews.as_view(), name='add_news'),
    path('news/<slug:news_slug>/', ShowNews.as_view(), name='show_news'),
    path('register/', register_user, name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    # path('register/', RegisterUser.as_view(), name='register'),
    # path('test/', test, name='test'),
]