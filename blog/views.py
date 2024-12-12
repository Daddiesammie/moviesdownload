import json
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.contrib import messages
from .models import Post, Category, Comment, Vote
from .forms import CommentForm
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


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

@login_required
@require_POST
def handle_vote(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    data = json.loads(request.body)
    action = data.get('action')
    
    # Get or create vote
    vote, created = Vote.objects.get_or_create(
        post=post,
        user=request.user,
        defaults={'vote_type': action}
    )
    
    # Handle vote change
    if not created and vote.vote_type != action:
        vote.vote_type = action
        vote.save()
    elif not created and vote.vote_type == action:
        vote.delete()
    
    # Get updated counts
    likes_count = post.vote_set.filter(vote_type='like').count()
    dislikes_count = post.vote_set.filter(vote_type='dislike').count()
    
    # Update post counts
    post.likes = likes_count
    post.dislikes = dislikes_count
    post.save()
    
    return JsonResponse({
        'status': 'success',
        'count': likes_count if action == 'like' else dislikes_count,
        'opposite_count': dislikes_count if action == 'like' else likes_count
    })


@login_required
@require_POST
def add_comment(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug)
    data = json.loads(request.body)
    
    comment = Comment.objects.create(
        post=post,
        user=request.user,
        content=data['content']
    )

    return JsonResponse({
        'status': 'success',
        'comment': {
            'id': comment.id,
            'content': comment.content,
            'user': comment.user.username,
            'created_at': comment.created_at.strftime('%B %d, %Y'),
            'can_delete': True
        }
    })


from django.http import JsonResponse

def get_comments(request, slug):
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.all().order_by('-created_at')
    
    comments_data = [{
        'id': comment.id,
        'content': comment.content,
        'user': comment.user.username,
        'created_at': comment.created_at.strftime('%B %d, %Y'),
        'can_delete': comment.user == request.user
    } for comment in comments]
    
    return JsonResponse({'comments': comments_data})

@login_required
@require_POST
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    
    # Check if user owns the comment
    if comment.user == request.user:
        comment.delete()
        return JsonResponse({'status': 'success'})
    
    return JsonResponse({'status': 'error'}, status=403)
