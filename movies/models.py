from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth.models import User

class Genre(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Content(models.Model):
    CONTENT_TYPE_CHOICES = [
        ('MOVIE', 'Movie'),
        ('SERIES', 'TV Series')
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    thumbnail_url = models.URLField()
    genres = models.ManyToManyField(Genre)
    release_year = models.IntegerField()
    content_type = models.CharField(max_length=6, choices=CONTENT_TYPE_CHOICES)
    download_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('movies:content_detail', kwargs={'slug': self.slug})

class Season(models.Model):
    series = models.ForeignKey(Content, on_delete=models.CASCADE, related_name='seasons')
    season_number = models.IntegerField()
    title = models.CharField(max_length=200)
    
    class Meta:
        unique_together = ['series', 'season_number']
        ordering = ['season_number']

    def __str__(self):
        return f"{self.series.title} - Season {self.season_number}"

class Episode(models.Model):
    season = models.ForeignKey(Season, on_delete=models.CASCADE, related_name='episodes')
    episode_number = models.IntegerField()
    title = models.CharField(max_length=200)
    description = models.TextField()
    video_url = models.URLField()
    download_count = models.IntegerField(default=0)
    
    class Meta:
        unique_together = ['season', 'episode_number']
        ordering = ['episode_number']

    def __str__(self):
        return f"S{self.season.season_number}E{self.episode_number} - {self.title}"

class Movie(models.Model):
    content = models.OneToOneField(Content, on_delete=models.CASCADE, related_name='movie')
    download_url = models.URLField(help_text="Direct download link for the movie", null=True)
    video_url = models.URLField()

    def __str__(self):
        return self.content.title


class Comment(models.Model):
    content = models.ForeignKey(Content, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(null=True)  # Changed from content to text
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Comment by {self.user.username} on {self.content.title}"

