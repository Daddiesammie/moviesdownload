from django.contrib import admin
from .models import Genre, Content, Season, Episode, Movie

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

class MovieInline(admin.StackedInline):
    model = Movie

class EpisodeInline(admin.TabularInline):
    model = Episode
    extra = 1

class SeasonInline(admin.TabularInline):
    model = Season
    extra = 1

@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ['title', 'content_type', 'release_year', 'download_count']
    list_filter = ['content_type', 'release_year', 'genres']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [MovieInline, SeasonInline]

    def get_inlines(self, request, obj=None):
        if obj and obj.content_type == 'MOVIE':
            return [MovieInline]
        elif obj and obj.content_type == 'SERIES':
            return [SeasonInline]
        return []

@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    list_display = ['series', 'season_number', 'title']
    inlines = [EpisodeInline]

@admin.register(Episode)
class EpisodeAdmin(admin.ModelAdmin):
    list_display = ['title', 'season', 'episode_number']
    list_filter = ['season__series']
