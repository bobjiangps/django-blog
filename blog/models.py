from django.db import models
from django.utils import timezone
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Visiable(models.Model):
    visible_options = (('0','public'),('1','private'))
    name = models.CharField(max_length=100, choices=visible_options, default=visible_options[0])
    #vis = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    #text = models.TextField()
    #text = RichTextField()
    text = RichTextUploadingField()
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)
    category = models.ForeignKey(Category,null=True, on_delete=models.SET_NULL)
    tag = models.ManyToManyField(Tag)
    visiable = models.ForeignKey(Visiable, null=True, on_delete=models.SET_NULL)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title


class Comment(models.Model):
    #user = models.ForeignKey(User)
    user = models.CharField(max_length=50)
    content = models.TextField()
    #parent为该评论的父评论，所以第一个参数为'self',当为空时表示为第一层级的评论
    #指定related_name='children'，这样可以父评论通过comment.children获取子评论，默认是通过comment.comment_set获取
    parent = models.ForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.SET_NULL)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content

    class Meta:
        ordering = ['-created_time']
