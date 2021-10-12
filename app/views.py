from django.utils.text import slugify
from django.views.generic import ListView, CreateView, TemplateView, DetailView

from app.models import Project


class IndexView(TemplateView):
    template_name = "app/pages/index.html"


class ProjectListView(ListView):
    model = Project
    context_object_name = "projects"
    template_name = "app/pages/project_list.html"


class ProjectDetailView(DetailView):
    model = Project
    context_object_name = "project"
    template_name = "app/pages/project_detail.html"


class ProjectCreateView(CreateView):
    model = Project
    template_name = ""
