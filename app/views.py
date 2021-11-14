import json
import mimetypes

from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, TemplateView, \
    DetailView, UpdateView, RedirectView

from app.enums import ProjectFileTypeChoices
from app.forms import UserForm, ProjectCreateForm, ProjectUpdateForm
from app.models import Project, FavoriteProject, ProjectFile
from app.utils.project_name_generator.generator import \
    generate_random_project_name


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
    paginate_by = 10


class PersonalProjectListView(LoginRequiredMixin, ListView):
    login_url = reverse_lazy("user-login")
    model = Project
    context_object_name = "projects"
    template_name = "app/pages/my_project_list.html"

    def get_queryset(self):
        return super(PersonalProjectListView, self).get_queryset().filter(
            creator=self.request.user)


class ProjectDetailView(LoginRequiredMixin, DetailView):
    login_url = reverse_lazy("user-login")
    model = Project
    context_object_name = "project"
    template_name = "app/pages/project_detail.html"
    slug_field = "slug"

    def get_context_data(self, **kwargs):
        context = super(ProjectDetailView, self).get_context_data(**kwargs)
        context["is_author"] = self.object.creator == self.request.user
        return context

    def get_object(self, queryset=None):
        project = super(ProjectDetailView, self).get_object(queryset)
        if project.is_private and project.creator != self.request.user:
            raise Http404()
        return project


class ProjectCreateView(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy("user-login")
    model = Project
    template_name = "app/pages/project_create.html"
    form_class = ProjectCreateForm

    def get_form_kwargs(self):
        form_kwargs = super(ProjectCreateView, self).get_form_kwargs()
        form_kwargs["user"] = self.request.user
        return form_kwargs

    def get_success_url(self):
        return reverse_lazy("ideas-list")


class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy("user-login")
    model = Project
    template_name = "app/pages/project_update.html"
    form_class = ProjectUpdateForm
    slug_field = "slug"

    def get(self, request, *args, **kwargs):
        project = self.get_object()
        if project.creator != self.request.user:
            return redirect(
                reverse_lazy("ideas-detail", kwargs={"slug": project.slug}))
        return super(ProjectUpdateView, self).get(request, *args, **kwargs)

    def get_form_kwargs(self):
        form_kwargs = super(ProjectUpdateView, self).get_form_kwargs()
        form_kwargs["user"] = self.request.user
        return form_kwargs

    def get_form(self, form_class=None):
        form = super(ProjectUpdateView, self).get_form(form_class)
        existing_project_file = ProjectFile.objects.filter(
            project_file_type=ProjectFileTypeChoices.ABLETON_PROJECT_FILE.name,
            project=self.object
        )
        if existing_project_file.exists():
            form.fields["notes"].initial = existing_project_file.get().notes
        return form

    def get_success_url(self):
        return reverse_lazy("ideas-detail", kwargs={"slug": self.object.slug})


class AddFavoriteView(LoginRequiredMixin, RedirectView):
    login_url = reverse_lazy("user-login")

    def get(self, request, *args, **kwargs):
        source_url = request.headers["Referer"]
        user = request.user
        redirect_url = HttpResponseRedirect(source_url)
        if not user or not user.is_authenticated:
            return redirect_url
        try:
            project = Project.objects.get(slug=kwargs["slug"])
        except Project.DoesNotExist:
            return redirect_url
        if project.is_private and user != project.creator:
            return redirect_url
        existing_favorite = FavoriteProject.objects.filter(user=user,
                                                           project=project)
        if existing_favorite.exists():
            existing_favorite.delete()
        else:
            FavoriteProject.objects.create(user=user, project=project)
        return redirect_url


def random_project_name_view(request):
    random_name = generate_random_project_name()
    data = {"name": random_name}
    if request.user.is_authenticated:
        return HttpResponse(json.dumps(data), content_type="application/json")
    else:
        return HttpResponse(status=403)


class DownloadAudioFileView(LoginRequiredMixin, View):
    login_url = reverse_lazy("user-login")

    def get(self, request, slug):
        project = Project.objects.get(slug=slug)
        if project.is_private and project.creator != self.request.user:
            raise Http404()
        audio_file = project.joined_files[
            ProjectFileTypeChoices.AUDIO_FILE.name]
        file_path = audio_file.file.path
        file_name = audio_file.name
        mime_type, _ = mimetypes.guess_type(file_path)
        file_content = audio_file.file.read()
        response = HttpResponse(file_content, content_type=mime_type)
        response['Content-Disposition'] = "attachment; filename={}".format(
            file_name)
        return response
