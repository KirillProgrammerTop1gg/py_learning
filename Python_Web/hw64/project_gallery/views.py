from django.shortcuts import render, redirect
from .models import Project, ProjectGallery
from .forms import ProjectForm, ProjectGalleryForm, AddImagesForm

def project_list(request):
    projects = Project.objects.all()
    return render(request, 'project_gallery/index.html', {'projects': projects})

def add_project(request):
    if request.method == 'POST':
        project_form = ProjectForm(request.POST)
        gallery_form = ProjectGalleryForm(request.POST, request.FILES)
        if project_form.is_valid() and gallery_form.is_valid():
            project = project_form.save()
            images = request.FILES.getlist('images')
            for img in images:
                ProjectGallery.objects.create(
                    project=project,
                    original_image=img,
                )
            return redirect('project_gallery:index')
    else:
        project_form = ProjectForm()
        gallery_form = ProjectGalleryForm()
        
    return render(request, 'project_gallery/add_project.html', {
        'project_form': project_form,
        'gallery_form': gallery_form
    })

def add_images(request):
    if request.method == 'POST':
        form = AddImagesForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.cleaned_data['project']
            images = request.FILES.getlist('images')
            for img in images:
                ProjectGallery.objects.create(
                    project=project,
                    original_image=img
                )
            return redirect('project_gallery:index')
    else:
        form = AddImagesForm()

    return render(request, 'project_gallery/add_images.html', {'form': form})
