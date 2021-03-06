# Generated by Django 3.0.8 on 2020-07-26 14:00

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('societies', '0004_auto_20200726_1359'),
    ]

    operations = [
        migrations.AddField(
            model_name='society',
            name='members',
            field=models.ManyToManyField(related_name='societies', through='societies.SocietyMembership', to=settings.AUTH_USER_MODEL, verbose_name='Members'),
        ),
    ]
