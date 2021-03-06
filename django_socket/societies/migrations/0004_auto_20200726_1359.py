# Generated by Django 3.0.8 on 2020-07-26 13:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('societies', '0003_socpost'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='society',
            name='members',
        ),
        migrations.AlterField(
            model_name='socpost',
            name='society',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='societies.Society'),
        ),
        migrations.CreateModel(
            name='SocietyMembership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_leader', models.BooleanField(default=False)),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='society_membership', to=settings.AUTH_USER_MODEL)),
                ('society', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='societies.Society')),
            ],
        ),
    ]
