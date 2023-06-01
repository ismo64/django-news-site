from typing import Any, Dict
from django.db import models
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.urls import reverse_lazy
from .models import New, Category
from django.db.models import Count
from .forms import AddNewsForm
from django.utils.text import slugify
from unidecode import unidecode
from django.views import generic
from .forms import AddNewsForm, RegisterUserForm, LoginUserForm
from .utils import DataMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView

# Create your views here.

class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'news/login.html'
    redirect_authenticated_user = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')
    

def register_user(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Регистрация прошла успешно')
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Ошибка регистрации')
    else:
        form = RegisterUserForm()
    
    return render(request, 'news/register.html', {'form': form, 'title': 'Регистрация'})

def logout_user(request):
    logout(request)
    return redirect('login')



# class RegisterUser(DataMixin, generic.CreateView):
#     form_class = RegisterUserForm
#     template_name = 'news/register.html'
#     success_url = reverse_lazy('home')

#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         c_def = self.get_user_context(title="Регистрация")
#         return dict(list(context.items()) + list(c_def.items()))
    
#     def form_valid(self, form):
#         user = form.save()
#         login(self.request, user)
#         return redirect('home')


class NewsHome(DataMixin, generic.ListView):
    model = New
    template_name = 'news/category.html'
    context_object_name = 'news'

    def get_queryset(self):
        return New.objects.filter(is_published=True).select_related('category')

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Главная страница')
        return dict(list(context.items()) + list(c_def.items()))

# def index(request):
#     news = New.objects.all()
#     categories = Category.objects.annotate(num_news=Count('news')).filter(num_news__gt=0)
#     context = {'news': news, 'title': 'Список новостей', 'categories': categories, 'cat_selected': 0}
#     return render(request, 'news/category.html', context=context)


class ShowNews(DataMixin, generic.DetailView):
    model = New
    template_name = 'news/show_news.html'
    slug_url_kwarg = 'news_slug'
    context_object_name = 'item'

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['object'].title)
        return dict(list(context.items()) + list(c_def.items()))
    
    def get_queryset(self):
        return New.objects.all().select_related('category').select_related('category')

# def show_news(request, news_slug):
#     news = get_object_or_404(New, slug=news_slug)
#     categories = Category.objects.annotate(num_news=Count('news')).filter(num_news__gt=0)
#     context = {
#         'item': news,
#         'title': news.title,
#         'categories': categories,
#     }

#     return render(request, 'news/show_news.html', context=context)

class NewsCategory(DataMixin, generic.ListView):
    model = New
    template_name = 'news/category.html'
    context_object_name = 'news'

    def get_queryset(self):
        return New.objects.filter(category_id=self.kwargs['cat_id']).select_related('category')
    
    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        cat_selected = self.get_queryset()[0].category
        c_def = self.get_user_context(cat_selected=cat_selected.id, title=cat_selected.title)
        return dict(list(context.items()) + list(c_def.items()))    

class ShowCategory(DataMixin, generic.DetailView):
    model = Category
    template_name = 'news/category.html'
    pk_url_kwarg = 'cat_id'

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['object'].title,
                                      cat_selected=context['object'].id)
        context['news'] = New.objects.filter(is_published=True, category_id=context['object'].id).select_related('category')
        return dict(list(context.items()) + list(c_def.items()))


# def get_category(request, cat_id):
#     news = New.objects.filter(category_id=cat_id)
#     categories = Category.objects.annotate(num_news=Count('news')).filter(num_news__gt=0)
#     category = Category.objects.get(id=cat_id)
#     context = {
#         'title': category.title,
#         'news': news,
#         'categories': categories,
#         'category': category,
#         'cat_selected': cat_id,
#     }

#     return render(request, 'news/category.html', context=context)

class AddNews(LoginRequiredMixin, DataMixin, generic.CreateView):
    form_class = AddNewsForm
    template_name = 'news/add_news.html'
    # login_url = 'login'

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context()
        return dict(list(context.items()) + list(c_def.items()))
    

# def add_news(request):
#     categories = Category.objects.annotate(num_news=Count('news')).filter(num_news__gt=0)
#     if request.method == 'POST':
#         form = AddNewsForm(request.POST, request.FILES)
#         if form.is_valid():
#             news = form.save()
#             print(news)
#             return redirect(news)
#     else:
#         form = AddNewsForm()
            
#     return render(request, 'news/add_news.html', {'form': form, 
#                                                   'categories': categories})
