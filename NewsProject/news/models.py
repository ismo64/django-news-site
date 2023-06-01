from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from unidecode import unidecode


# Create your models here.

class New(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название')
    content = models.TextField(blank=True, verbose_name='Содержимое')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время добавления')
    updatet_at = models.DateTimeField(auto_now=True, verbose_name='Время изменения')
    photo = models.ImageField(upload_to='media/%Y/%m/%d', verbose_name='Изображение')
    is_published = models.BooleanField(default=False, verbose_name='Опубликовано')
    slug = models.SlugField(max_length=100, unique=True, db_index=True, verbose_name='URL')
    category = models.ForeignKey('Category', related_name='news', on_delete=models.PROTECT, null=True, verbose_name='Категория')

    class Meta:
        verbose_name_plural = 'Новости'
        ordering = ('id',)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode('-'.join(self.title.split())))
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('show_news', kwargs={'news_slug': self.slug})
    
    def __str__(self):
        return f'{self.title}'

class Category(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название')
    slug = models.SlugField(max_length=100, unique=True, db_index=True, verbose_name='URL')


    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('title', )

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_id': self.id})

    def __str__(self):
        return f'{self.title}'
    

