from django import forms
from .models import Post
from ckeditor.fields import RichTextFormField
from django.forms import ModelForm


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        #content = RichTextFormField()
        fields = ('title', 'text', 'category', 'tag', 'visiable')
        #fields = '__all__'


