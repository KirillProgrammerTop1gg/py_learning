from django.views.decorators.cache import cache_page
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from .models import Post, Comment
from .forms import CommentForm

@cache_page(300)
def post_list(request):
    posts = Post.objects.all().select_related('author')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, post_id):
    post = get_object_or_404(Post.objects.prefetch_related('comments__author'), id=post_id)
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
            
        five_minutes_ago = timezone.now() - timedelta(minutes=5)
        recent_comments_count = Comment.objects.filter(author=request.user, created_at__gte=five_minutes_ago).count()
        if recent_comments_count >= 3:
            messages.error(request, 'Ви перевищили ліміт коментарів. Зачекайте 5 хвилин перед тим, як залишити наступний.')
            return redirect('post_detail', post_id=post.id)
            
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', post_id=post.id)
    else:
        form = CommentForm()
    
    return render(request, 'blog/post_detail.html', {
        'post': post,
        'form': form
    })

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('post_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('post_list')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
    return redirect('post_list')