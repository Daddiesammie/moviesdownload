from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    path('<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),
    path('<slug:post_slug>/comment/', views.add_comment, name='add_comment'),
    # Add this to your existing urlpatterns
    path('post/<int:post_id>/vote/', views.handle_vote, name='handle_vote'),
]
