import json
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.db.models import Q
from .models import Content, Season, Episode, Movie
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import ensure_csrf_cookie

class ContentListView(ListView):
    model = Content
    template_name = 'movies/content_list.html'
    context_object_name = 'contents'
    paginate_by = 12

class MovieListView(ListView):
    template_name = 'movies/movie_list.html'
    context_object_name = 'movies'
    paginate_by = 12

    def get_queryset(self):
        return Content.objects.filter(content_type='MOVIE')

class SeriesListView(ListView):
    template_name = 'movies/series_list.html'
    context_object_name = 'series'
    paginate_by = 12

    def get_queryset(self):
        return Content.objects.filter(content_type='SERIES')

class ContentDetailView(DetailView):
    model = Content
    template_name = 'movies/content_detail.html'
    context_object_name = 'content'

    def get_template_names(self):
        if self.object.content_type == 'MOVIE':
            return ['movies/movie_detail.html']
        return ['movies/series_detail.html']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object.content_type == 'SERIES':
            context['seasons'] = self.object.seasons.all()
        return context

class SeasonDetailView(DetailView):
    template_name = 'movies/season_detail.html'
    context_object_name = 'season'

    def get_object(self):
        series = get_object_or_404(Content, 
                                 slug=self.kwargs['series_slug'], 
                                 content_type='SERIES')
        return get_object_or_404(Season, 
                               series=series, 
                               season_number=self.kwargs['season_number'])

def movie_download(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    movie.content.download_count += 1
    movie.content.save()
    return redirect(movie.download_url) 

def episode_download(request, episode_id):
    episode = get_object_or_404(Episode, id=episode_id)
    episode.download_count += 1
    episode.save()
    return redirect(episode.video_url)

class ContentSearchView(ListView):
    model = Content
    template_name = 'movies/content_list.html'
    context_object_name = 'contents'
    paginate_by = 12

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Content.objects.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query)
            )
        return Content.objects.none()
    
@require_POST
@ensure_csrf_cookie
def handle_content_vote(request, content_id):
    content = get_object_or_404(Content, id=content_id)
    data = json.loads(request.body)
    action = data.get('action')

    if action == 'like':
        content.likes += 1
    elif action == 'dislike':
        content.dislikes += 1
    content.save()

    return JsonResponse({
        'status': 'success',
        'count': content.likes if action == 'like' else content.dislikes
    })
