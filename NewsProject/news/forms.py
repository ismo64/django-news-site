from django import forms
from .models import New, Category
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.utils.text import slugify
from unidecode import unidecode
from django.core.exceptions import ValidationError
from captcha.fields import CaptchaField
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from ckeditor.widgets import CKEditorWidget
import re

class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    captcha = CaptchaField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'captcha')

class AddNewsForm(forms.ModelForm):
    class Meta:
        model = New
        fields = ('title', 'content', 'photo', 'is_published', 'category',)
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'cols': 60, 'rows': 10}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if re.match('\d', title):
            raise ValidationError('Название не должно начинаться с цифры')
        return title
    
# class AddNewsForm(forms.Form):
#     title = forms.CharField(label='Заголовок', widget=forms.TextInput(attrs={'class': 'form-control'}))
#     content = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'cols': 60, 'rows': 10}), label='Содержание')
#     photo = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control'}))
#     is_published = forms.BooleanField(required=False, initial=True, label='Опубликовать')
#     category = forms.ModelChoiceField(queryset=Category.objects.all(), label='Категории',
#                                       empty_label='Выберите категорию')

#     def clean_title(self):
#         title = self.cleaned_data['title']
#         if len(title) > 100:
#             raise ValidationError('Длина превышает 200 символов')
#         return title