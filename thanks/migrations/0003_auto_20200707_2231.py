# Generated by Django 3.0.5 on 2020-07-07 13:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('thanks', '0002_auto_20200707_2126'),
    ]

    operations = [
        migrations.RenameField(
            model_name='thanks',
            old_name='recipient',
            new_name='recipients',
        ),
    ]