# Generated by Django 3.0.5 on 2020-07-07 21:58

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('thanks', '0003_auto_20200707_2231'),
    ]

    operations = [
        migrations.AddField(
            model_name='thanks',
            name='approval',
            field=models.IntegerField(choices=[(0, '承認待ち'), (1, '承認済み')], default=0),
        ),
        migrations.AddField(
            model_name='thanks',
            name='date_posted',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
