# Generated by Django 5.1.4 on 2024-12-06 23:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('slug', models.SlugField(unique=True)),
                ('description', models.TextField()),
                ('thumbnail_url', models.URLField()),
                ('release_year', models.IntegerField()),
                ('content_type', models.CharField(choices=[('MOVIE', 'Movie'), ('SERIES', 'TV Series')], max_length=6)),
                ('download_count', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('genres', models.ManyToManyField(to='movies.genre')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video_url', models.URLField()),
                ('content', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='movie', to='movies.content')),
            ],
        ),
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('season_number', models.IntegerField()),
                ('title', models.CharField(max_length=200)),
                ('series', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seasons', to='movies.content')),
            ],
            options={
                'ordering': ['season_number'],
                'unique_together': {('series', 'season_number')},
            },
        ),
        migrations.CreateModel(
            name='Episode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('episode_number', models.IntegerField()),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('video_url', models.URLField()),
                ('download_count', models.IntegerField(default=0)),
                ('season', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='episodes', to='movies.season')),
            ],
            options={
                'ordering': ['episode_number'],
                'unique_together': {('season', 'episode_number')},
            },
        ),
    ]