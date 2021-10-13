from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify

from app.enums import VALID_AUDIO_FILE_TYPES, ProjectFileTypeChoices


class Project(models.Model):
    name = models.CharField(max_length=100)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(blank=True, null=True)
    modified_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("project-detail", kwargs={"slug": slugify(self.name)})

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
        self.modified_at = timezone.now()
        return super(Project, self).save(*args, **kwargs)

    @property
    def joined_files(self):
        file_types = {
            ProjectFileTypeChoices.AUDIO_FILE.name: False,
            ProjectFileTypeChoices.MUSIC_SHEET.name: False,
            ProjectFileTypeChoices.ABLETON_PROJECT_FILE.name: False
                      }
        for file in self.files.all():
            file_types[file.project_file_type] = file
        return file_types


class ProjectFile(models.Model):
    name = models.CharField(max_length=60)
    file = models.FileField(upload_to="media/")
    uploaded_at = models.DateTimeField(blank=True, null=True)
    project_file_type = models.CharField(max_length=255, choices=ProjectFileTypeChoices.choices)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="files")

    def __str__(self):
        return "{} - {}".format(self.name, self.project_file_type)

    def clean(self):
        super(ProjectFile, self).clean()
        if self.project_file_type == ProjectFileTypeChoices.AUDIO_FILE.name:
            if self.is_valid_audio_file(self.file):
                pass
            else:
                raise ValidationError("Not a valid file type")

    @staticmethod
    def is_valid_audio_file(file):
        for file_type, mime_type in VALID_AUDIO_FILE_TYPES.items():
            try:
                if file._file.content_type == mime_type:
                    return True
            except AttributeError:
                pass
        return False

    def save(self, *args, **kwargs):
        if not self.id:
            self.uploaded_at = timezone.now()
        return super(ProjectFile, self).save(*args, **kwargs)


class FavoriteProject(models.Model):
    user = models.ForeignKey(User, related_name="favorites", on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
