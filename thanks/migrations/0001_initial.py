# Generated by Django 3.0.5 on 2020-07-06 13:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user', '0006_auto_20200702_2313'),
    ]

    operations = [
        migrations.CreateModel(
            name='Thanks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('good_count', models.IntegerField()),
                ('giver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('recipient', models.ManyToManyField(to='user.Profile')),
            ],
        ),
    ]