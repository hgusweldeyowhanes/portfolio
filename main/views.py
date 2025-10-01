from django.shortcuts import render, get_object_or_404
from .models import Project, Skills, Experience

def home(request):
    projects = Project.objects.filter(featured=True).order_by('-created_at')[:6]
    skills = Skills.objects.all()[:10]
    experiences = Experience.objects.all()[:3]
    return render(request, 'home.html', {
        'projects': projects,
        'skills': skills,
        'experiences': experiences,
    })

# Project List
def project_list(request):
    projects = Project.objects.all()
    return render(request, 'project_list.html', {'projects': projects})

# Project Detail
def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug)
    return render(request, 'project_detail.html', {'project': project})

# Skills List
def skills_list(request):
    skills = Skills.objects.all()
    return render(request, 'skills_list.html', {'skills': skills})

# Experience List
def experience_list(request):
    experiences = Experience.objects.all()
    return render(request, 'experience_list.html', {'experiences': experiences})
