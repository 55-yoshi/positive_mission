# Generated by Django 3.0.5 on 2020-07-19 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mission', '0008_mission_participants_limit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mission',
            name='success_exp',
            field=models.IntegerField(default=0),
        ),
    ]