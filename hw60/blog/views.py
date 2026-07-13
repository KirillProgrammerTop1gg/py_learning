from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import F
from .models import BlogPost, Comment
from portfolio.models import Category, Technology

from django.db.models import Q

def blog_list_view(request):
    posts = BlogPost.objects.all().select_related('category').prefetch_related('technologies')
    
    query = request.GET.get('q')
    if query:
        query = query.strip()
        posts = posts.filter(
            Q(title__icontains=query) |
            Q(category__name__icontains=query) |
            Q(technologies__name__icontains=query)
        ).distinct()
        
    context = {
        'posts': posts,
        'query': query,
    }
    return render(request, 'blog/blog_list.html', context)


def blog_detail_view(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)
    
    # Atomically increment page views count
    BlogPost.objects.filter(pk=post.pk).update(views_count=F('views_count') + 1)
    post.refresh_from_db()
    
    comments = post.comments.all().select_related('user').order_by('created_at')
    
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, "Будь ласка, увійдіть у систему, щоб залишити коментар.")
            return redirect('orders:login')
            
        comment_text = request.POST.get('text', '').strip()
        if len(comment_text) > 1000:
            messages.error(request, "Текст коментаря занадто довгий (максимум 1000 символів).")
        elif comment_text:
            Comment.objects.create(
                post=post,
                user=request.user,
                text=comment_text
            )
            messages.success(request, "Коментар успішно додано!")
            return redirect('blog:detail', slug=post.slug)
        else:
            messages.error(request, "Текст коментаря не може бути порожнім.")
            
    context = {
        'post': post,
        'comments': comments,
    }
    return render(request, 'blog/blog_detail.html', context)
