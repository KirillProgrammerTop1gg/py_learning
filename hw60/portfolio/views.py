from django.shortcuts import render, get_object_or_404
from .models import Project, Skill, Experience, Technology

from orders.models import Review

def home(request):
    # Homepage without full projects list
    skills = Skill.objects.select_related('category')
    experiences = Experience.objects.all()
    reviews = Review.objects.select_related('user', 'order').order_by('-created_at')
    
    context = {
        'skills': skills,
        'experiences': experiences,
        'reviews': reviews,
    }
    return render(request, 'portfolio/home.html', context)

def projects_list(request):
    # Separate page with all projects as cards/gallery with technology filtering
    projects = Project.objects.all().prefetch_related('technologies')
    technologies = Technology.objects.all()
    
    context = {
        'projects': projects,
        'technologies': technologies,
    }
    return render(request, 'portfolio/projects_list.html', context)

from django.db.models import F

def project_detail(request, pk):
    # Detailed page for a single project inside the premium editor window layout
    project = get_object_or_404(Project.objects.prefetch_related('technologies__category'), pk=pk)
    Project.objects.filter(pk=pk).update(views_count=F('views_count') + 1)
    project.refresh_from_db()
    
    context = {
        'project': project,
    }
    return render(request, 'portfolio/project_detail.html', context)
