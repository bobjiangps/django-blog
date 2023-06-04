from django.db import models
from django.utils import timezone


class CalledStat(models.Model):
    name = models.CharField(max_length=100)
    amount = models.PositiveIntegerField(default=0)
    create_date = models.DateTimeField(default=timezone.now)
    update_date = models.DateTimeField(default=timezone.now)

    def increase_views(self):
        self.update_date = timezone.now()
        self.amount += 1
        self.save(update_fields=['amount', 'update_date'])

    def __str__(self):
        return self.name


class Debug(models.Model):
    name = models.CharField(max_length=100)
    create_time = models.DateTimeField(default=timezone.now)
    update_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name
