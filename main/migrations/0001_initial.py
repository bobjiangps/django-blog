# Generated by Django 2.1.5 on 2019-10-14 16:39

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Visitor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(max_length=30)),
                ('region', models.CharField(blank=True, max_length=1000, null=True)),
                ('agent', models.CharField(max_length=1000)),
                ('page', models.CharField(max_length=100)),
                ('views', models.PositiveIntegerField(default=0)),
                ('record_date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]
