# Generated by Django 3.2.4 on 2023-10-05 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum_app', '0010_post_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.TextField(max_length=200),
        ),
    ]
