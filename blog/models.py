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

    # 阅读数(>0的数)
    views = models.PositiveIntegerField(default=0)
    # 增加阅读数的方法
    def increase_views(self):
        self.views += 1
        # update_fields 只更新数据库中的views
        self.save(update_fields=['views'])


class Visitor(models.Model):
    ip = models.CharField(max_length=30)
    region = models.CharField(max_length=1000, blank=True, null=True)
    agent = models.CharField(max_length=1000)
    page = models.CharField(max_length=100)
    referer = models.CharField(max_length=500, blank=True, null=True)
    views = models.PositiveIntegerField(default=0)
    record_date = models.DateTimeField(default=timezone.now)
    update_date = models.DateTimeField(default=timezone.now)

    def increase_views(self):
        self.update_date = timezone.now()
        self.views += 1
        self.save(update_fields=['views', 'update_date'])
