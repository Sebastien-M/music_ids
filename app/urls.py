from django.urls import path

from app.views import ProjectListView, IndexView, ProjectDetailView, UserCreateView, UserLoginView, UserLogOutView, \
    ProjectCreateView, PersonalProjectListView

urlpatterns = [
    path("", view=IndexView.as_view(), name="index-view"),
    path("login/", view=UserLoginView.as_view(), name="user-login"),
    path("logout/", view=UserLogOutView.as_view(), name="user-logout"),
    path("ideas/", view=ProjectListView.as_view(), name="ideas-list"),
    path("personal_ideas/", view=PersonalProjectListView.as_view(), name="personal-ideas-list"),
    path("new_user/", view=UserCreateView.as_view(), name="user-create"),
    path("ideas/<int:pk>", view=ProjectDetailView.as_view(), name="ideas-detail"),
    path("ideas/create/", view=ProjectCreateView.as_view(), name="ideas-create"),
]