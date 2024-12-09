from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    path('', views.ContentListView.as_view(), name='content_list'),
    path('movies/', views.MovieListView.as_view(), name='movie_list'),
    path('series/', views.SeriesListView.as_view(), name='series_list'),
    path('content/<slug:slug>/', views.ContentDetailView.as_view(), name='content_detail'),
    path('series/<slug:series_slug>/season/<int:season_number>/', 
         views.SeasonDetailView.as_view(), name='season_detail'),
    path('download/movie/<int:movie_id>/', views.movie_download, name='movie_download'),
    path('download/episode/<int:episode_id>/', views.episode_download, name='episode_download'),
    path('search/', views.ContentSearchView.as_view(), name='content_search'),
    # Add to urlpatterns
    path('content/<int:content_id>/vote/', views.handle_content_vote, name='handle_content_vote'),
]