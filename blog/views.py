import json
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.contrib import messages
from .models import Post, Category, Comment
from .forms import CommentForm
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import ensure_csrf_cookie

# Add these new views
@require_POST
@ensure_csrf_cookie
def handle_vote(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    data = json.loads(request.body)
    action = data.get('action')

    if action == 'like':
        post.likes += 1
    elif action == 'dislike':
        post.dislikes += 1
    post.save()

    return JsonResponse({
        'status': 'success',
        'count': post.likes if action == 'like' else post.dislikes
    })


class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 10

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        return context

def add_comment(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            messages.success(request, 'Comment added successfully!')
            return redirect('blog:post_detail', slug=post_slug)
    return redirect('blog:post_detail', slug=post_slug)
