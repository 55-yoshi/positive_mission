# Generated by Django 3.0.5 on 2020-06-29 21:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_auto_20200630_0637'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='success_count',
            field=models.IntegerField(default=0),
        ),
    ]
