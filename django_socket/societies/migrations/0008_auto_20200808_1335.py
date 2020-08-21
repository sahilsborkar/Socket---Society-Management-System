# Generated by Django 3.0.8 on 2020-08-08 13:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('societies', '0007_auto_20200728_1355'),
    ]

    operations = [
        migrations.AlterField(
            model_name='societyprofile',
            name='society',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to='societies.Society'),
        ),
        migrations.CreateModel(
            name='SocComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('date_posted', models.DateTimeField(default=django.utils.timezone.now)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='societies.SocPost')),
            ],
        ),
    ]
