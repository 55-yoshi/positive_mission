# Generated by Django 3.0.5 on 2020-07-07 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('thanks', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='thanks',
            name='good_count',
            field=models.IntegerField(default=0),
        ),
    ]
