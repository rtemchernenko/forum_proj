# Generated by Django 3.2.4 on 2023-09-26 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum_app', '0003_alter_forum_slug_alter_post_slug_alter_thread_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forum',
            name='slug',
            field=models.SlugField(blank=True, max_length=100, unique=True),
        ),
    ]