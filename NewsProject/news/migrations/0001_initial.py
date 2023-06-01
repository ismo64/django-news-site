# Generated by Django 4.2.1 on 2023-05-19 04:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Название')),
                ('slug', models.SlugField(max_length=100, unique=True, verbose_name='URL')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
                'ordering': ('title',),
            },
        ),
        migrations.CreateModel(
            name='New',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Название')),
                ('content', models.TextField(blank=True, verbose_name='Содержимое')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Время добавления')),
                ('updatet_at', models.DateTimeField(auto_now=True, verbose_name='Время изменения')),
                ('photo', models.ImageField(upload_to='media/%Y/%m/%d', verbose_name='Изображение')),
                ('is_published', models.BooleanField(default=False, verbose_name='Опубликовано')),
                ('slug', models.SlugField(max_length=100, unique=True, verbose_name='URL')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='news', to='news.category', verbose_name='Категория')),
            ],
            options={
                'verbose_name_plural': 'Новости',
                'ordering': ('id',),
            },
        ),
    ]