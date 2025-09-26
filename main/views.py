from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Project, Skills, Experience

# ---------------------------
# PROJECT VIEWS
# ---------------------------
from django.shortcuts import render
from .models import Project, Skills

def home(request):
    projects = Project.objects.all()  # get all projects
    skills = Skills.objects.all()     # get all skills if needed
    context = {
        "projects": projects,
        "skills": skills
    }
    return render(request, "base.html", context)

class ProjectListView(ListView):
    model = Project
    template_name = 'project_list.html'
    context_object_name = 'projects'
    paginate_by = 10  # optional pagination

class ProjectDetailView(DetailView):
    model = Project
    template_name = 'project_detail.html'
    context_object_name = 'project'

    # slug field is used for lookup
    def get_object(self):
        return get_object_or_404(Project, slug=self.kwargs.get('slug'))

# ---------------------------
# SKILLS VIEWS
# ---------------------------
class SkillsListView(ListView):
    model = Skills
    template_name = 'skills_list.html'
    context_object_name = 'skills'
    paginate_by = 20

class SkillsDetailView(DetailView):
    model = Skills
    template_name = 'skills_detail.html'
    context_object_name = 'skill'

# ---------------------------
# EXPERIENCE VIEWS
# ---------------------------
class ExperienceListView(ListView):
    model = Experience
    template_name = 'experience_list.html'
    context_object_name = 'experiences'
    paginate_by = 10

class ExperienceDetailView(DetailView):
    model = Experience
    template_name = 'experience_detail.html'
    context_object_name = 'experience'
