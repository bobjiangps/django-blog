# Generated by Django 2.2.13 on 2021-02-04 15:51

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0002_auto_20210123_1651'),
    ]

    operations = [
        migrations.CreateModel(
            name='TransferRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_of_occurrence', models.DateTimeField(default=django.utils.timezone.now)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=8)),
                ('comment', models.CharField(blank=True, max_length=500, null=True)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('currency', models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounting.Currency')),
                ('from_account', models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='from_account', to='accounting.Account')),
                ('to_account', models.ForeignKey(default=2, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='to_account', to='accounting.Account')),
            ],
            options={
                'ordering': ['-time_of_occurrence'],
            },
        ),
    ]
