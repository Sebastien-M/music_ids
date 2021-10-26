from django.urls import path

from app.views import ProjectListView, IndexView, ProjectDetailView, \
    UserCreateView, UserLoginView, UserLogOutView, \
    ProjectCreateView, ProjectUpdateView, PersonalProjectListView, \
    random_project_name_view, AddFavoriteView

urlpatterns = [
    path("", view=IndexView.as_view(), name="index-view"),
    path("login/", view=UserLoginView.as_view(), name="user-login"),
    path("logout/", view=UserLogOutView.as_view(), name="user-logout"),
    path("ideas/", view=ProjectListView.as_view(), name="ideas-list"),
    path("personal_ideas/", view=PersonalProjectListView.as_view(),
         name="personal-ideas-list"),
    path("new_user/", view=UserCreateView.as_view(), name="user-create"),
    path("ideas/<slug:slug>", view=ProjectDetailView.as_view(),
         name="ideas-detail"),
    path("ideas/create/", view=ProjectCreateView.as_view(),
         name="ideas-create"),
    path("ideas/update/<slug:slug>", view=ProjectUpdateView.as_view(),
         name="ideas-update"),
    path("ideas/favorite/<slug:slug>", view=AddFavoriteView.as_view(),
         name="ideas-favorite"),
    path("random_project_name/", view=random_project_name_view,
         name="random-project-name")
]
