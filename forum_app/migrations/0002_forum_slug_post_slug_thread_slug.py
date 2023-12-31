# Generated by Django 4.2.3 on 2023-09-25 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='forum',
            name='slug',
            field=models.SlugField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='slug',
            field=models.SlugField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='thread',
            name='slug',
            field=models.SlugField(max_length=100, null=True),
        ),
    ]
