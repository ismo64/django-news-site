from django.contrib import admin
from django.utils.safestring import mark_safe
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget


# Register your models here.
from .models import New, Category


class NewsAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = New
        fields = '__all__'

class NewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'title', 'created_at', 'get_photo', 'is_published')
    list_display_links = ('id', 'title')
    search_fields = ('title',)
    list_editable = ('category', 'is_published',)
    list_filter = ('created_at',)
    prepopulated_fields = {"slug": ("title",)}
    fields = ('title', 'content', 'photo', 'get_photo', 'slug', 'created_at', 'is_published')
    readonly_fields = ('created_at', 'get_photo')
    form = NewsAdminForm

    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{ obj.photo.url }" width="75">')
        else:
            return 'Фото нет'
    
    get_photo_description = 'Миниатюра'

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    list_filter = ('id', 'title')
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(New, NewsAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.site_title = 'Страница Администратора'
admin.site.site_header = 'Страница Администратора'