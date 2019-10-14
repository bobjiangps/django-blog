from django.db import models
from django.utils import timezone


class Visitor(models.Model):
    ip = models.CharField(max_length=30)
    region = models.CharField(max_length=1000, blank=True, null=True)
    agent = models.CharField(max_length=1000)
    page = models.CharField(max_length=100)
    views = models.PositiveIntegerField(default=0)
    record_date = models.DateTimeField(default=timezone.now)
    update_date = models.DateTimeField(default=timezone.now)

    def increase_views(self):
        self.update_date = timezone.now()
        self.views += 1
        self.save(update_fields=['views', 'update_date'])
