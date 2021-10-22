from django import forms
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import TemporaryUploadedFile
from django.forms import ModelForm
from django.utils import timezone

from app.enums import VALID_AUDIO_FILE_TYPES, ProjectFileTypeChoices
from app.models import MidUser, Project, ProjectFile


class UserForm(UserCreationForm):
    class Meta:
        model = MidUser
        field_classes = {'username': UsernameField}
        fields = ("username", "first_name", "last_name", "email", "password1", "password2")

    def is_valid(self):
        return super(UserForm, self).is_valid()


class ProjectCreateForm(ModelForm):
    class Meta:
        model = Project
        fields = ("name", "audio_file")

    name = forms.CharField(label="Nom du projet")
    audio_file = forms.FileField(label="Fichier audio")
    music_sheet = forms.FileField(label="Tablature", required=False)
    ableton_project_file = forms.FileField(label="Projet Ableton", required=False)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super(ProjectCreateForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):

        audio_file = self.cleaned_data.get("audio_file")
        music_sheet = self.cleaned_data.get("music_sheet")
        ableton_project_file = self.cleaned_data.get("ableton_project_file")

        project = Project.objects.create(name=self.cleaned_data.get("name"), creator=self.user,
                                         created_at=timezone.now())
        ProjectFile.objects.create(name=audio_file._name,
                                   file=audio_file,
                                   uploaded_at=timezone.now(),
                                   project_file_type=ProjectFileTypeChoices.AUDIO_FILE.name,
                                   project=project)
        ProjectFile.objects.create(name=music_sheet._name,
                                   file=music_sheet,
                                   uploaded_at=timezone.now(),
                                   project_file_type=ProjectFileTypeChoices.MUSIC_SHEET.name,
                                   project=project)
        ProjectFile.objects.create(name=ableton_project_file._name,
                                   file=ableton_project_file,
                                   uploaded_at=timezone.now(),
                                   project_file_type=ProjectFileTypeChoices.ABLETON_PROJECT_FILE.name,
                                   project=project)
        return Project

    def is_valid(self):
        is_valid = super(ProjectCreateForm, self).is_valid()
        audio_file = self.cleaned_data.get("audio_file")
        if not audio_file or not self.is_valid_audio_file(audio_file):
            self.add_error("audio_file", ValidationError("Vous devez choisir un fichier audio"))
            is_valid = False
        return is_valid

    @staticmethod
    def is_valid_audio_file(file: TemporaryUploadedFile) -> bool:
        for file_type, mime_type in VALID_AUDIO_FILE_TYPES.items():
            try:
                if file.content_type == mime_type:
                    return True
            except AttributeError:
                pass
        return False
