# Generated by Django 2.1.5 on 2019-10-14 22:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_visitor_update_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='visitor',
            name='referer',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]