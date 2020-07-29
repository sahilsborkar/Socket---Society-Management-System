# Generated by Django 3.0.8 on 2020-07-28 12:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('societies', '0005_society_members'),
    ]

    operations = [
        migrations.AlterField(
            model_name='society',
            name='name',
            field=models.CharField(max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='societymembership',
            name='society',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='society_membership', to='societies.Society'),
        ),
        migrations.CreateModel(
            name='SocietyProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(default='default.jpg', upload_to='society_profile_pics')),
                ('society', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='societies.Society')),
            ],
        ),
    ]