from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, TemplateView, DetailView

from app.forms import UserForm, ProjectCreateForm
from app.models import Project


class UserCreateView(CreateView):
    model = User
    form_class = UserForm
    template_name = "app/pages/user_create.html"

    def get_success_url(self):
        return reverse("index-view")


class UserLoginView(LoginView):
    template_name = "app/pages/user_login.html"

    def get_success_url(self):
        return reverse("index-view")


class UserLogOutView(View):

    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse_lazy("index-view"))


class IndexView(TemplateView):
    template_name = "app/pages/index.html"


class ProjectListView(LoginRequiredMixin, ListView):
    login_url = reverse_lazy("user-login")
    model = Project
    context_object_name = "projects"
    template_name = "app/pages/project_list.html"


class ProjectDetailView(LoginRequiredMixin, DetailView):
    login_url = reverse_lazy("user-login")
    model = Project
    context_object_name = "project"
    template_name = "app/pages/project_detail.html"


class ProjectCreateView(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy("user-login")
    model = Project
    template_name = "app/pages/project_create.html"
    form_class = ProjectCreateForm

    def get_form_kwargs(self):
        form_kwargs = super(ProjectCreateView, self).get_form_kwargs()
        form_kwargs["user"] = self.request.user
        return form_kwargs
