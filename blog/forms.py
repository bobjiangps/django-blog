from django import forms
from .models import Post
from ckeditor.fields import RichTextFormField
from django.forms import ModelForm
from blog.models import Comment


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        #content = RichTextFormField()
        fields = ('title', 'text', 'category', 'tag', 'visiable')
        #fields = '__all__'


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('content', 'parent', 'user', 'post')
