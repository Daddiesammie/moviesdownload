# Generated by Django 5.1.4 on 2024-12-08 01:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0002_movie_download_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='content',
            name='dislikes',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='content',
            name='likes',
            field=models.IntegerField(default=0),
        ),
    ]
