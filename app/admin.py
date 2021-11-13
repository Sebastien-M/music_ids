from django.contrib import admin

from app.models import Project, ProjectFile, MidUser


class ProjectFileInline(admin.StackedInline):
    model = ProjectFile


class ProjectAdmin(admin.ModelAdmin):
    model = Project
    inlines = [ProjectFileInline]


admin.site.register(Project, ProjectAdmin)
admin.site.register(MidUser)
admin.site.register(ProjectFile)
