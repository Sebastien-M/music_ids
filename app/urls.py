from django.urls import path

from app.views import ProjectListView, IndexView, ProjectDetailView

urlpatterns = [
    path("", view=IndexView.as_view(), name="index-view"),
    path("ideas/", view=ProjectListView.as_view(), name="ideas-list"),
    path("ideas/<int:pk>", view=ProjectDetailView.as_view(), name="ideas-detail"),
]