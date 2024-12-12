from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    path('<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),
    path('<slug:post_slug>/comment/', views.add_comment, name='add_comment'),
    path('post/<int:post_id>/vote/', views.handle_vote, name='handle_vote'),
    path('post/<slug:slug>/comments/', views.get_comments, name='get_comments'),
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
]
