from urllib.request import urlretrieve

from django import forms
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import TemporaryUploadedFile
from django.forms import ModelForm
from django.utils import timezone

from app.enums import VALID_AUDIO_FILE_TYPES, ProjectFileTypeChoices, \
    ProjectKeyChoices
from app.models import MidUser, Project, ProjectFile


class UserForm(UserCreationForm):
    description = forms.CharField(widget=forms.Textarea,
                                  label="Quelques mots sur vous",
                                  required=False)

    class Meta:
        model = MidUser
        field_classes = {'username': UsernameField}
        fields = ("username", "first_name", "last_name", "email", "password1",
                  "password2", "description")

    def is_valid(self):
        return super(UserForm, self).is_valid()

    def save(self, commit=True):
        user = super(UserForm, self).save(commit)
        file_name = "{}.svg".format(user.username)
        url = "https://avatars.dicebear.com/api/croodles-neutral/{}".format(
            file_name
        )
        profile_pic_response = urlretrieve(url)
        profile_pic = open(profile_pic_response[0])
        self.instance.picture.save(file_name, profile_pic)
        return user


class ProjectCreateForm(ModelForm):
    class Meta:
        model = Project
        fields = (
            "name", "audio_file", "key", "tempo", "is_private", "description")

    name = forms.CharField(label="Nom du projet")
    audio_file = forms.FileField(label="Fichier audio")
    description = forms.CharField(widget=forms.Textarea,
                                  label="Description",
                                  required=False)
    key = forms.ChoiceField(choices=ProjectKeyChoices.choices,
                            label="Tonalité")
    is_private = forms.BooleanField(label="Privé", required=False)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super(ProjectCreateForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        audio_file = self.cleaned_data.get("audio_file")
        project = Project.objects.create(name=self.cleaned_data.get("name"),
                                         creator=self.user,
                                         description=self.cleaned_data.get(
                                             "description"),
                                         created_at=timezone.now())
        ProjectFile.objects.create(name=audio_file._name,
                                   file=audio_file,
                                   uploaded_at=timezone.now(),
                                   project_file_type=ProjectFileTypeChoices.AUDIO_FILE.name,
                                   project=project)
        return Project

    def is_valid(self):
        is_valid = super(ProjectCreateForm, self).is_valid()
        audio_file = self.cleaned_data.get("audio_file")
        if not audio_file or not self.is_valid_audio_file(audio_file):
            self.add_error("audio_file", ValidationError(
                "Vous devez choisir un fichier audio"))
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


class ProjectUpdateForm(ModelForm):
    class Meta:
        model = Project
        fields = (
            "name", "audio_file", "is_private", "key", "tempo", "description")

    name = forms.CharField(label="Nom du projet")
    audio_file = forms.FileField(label="Fichier audio", required=False)
    description = forms.CharField(widget=forms.Textarea,
                                  label="Description",
                                  required=False)
    is_private = forms.BooleanField(label="Privé", required=False)
    key = forms.ChoiceField(choices=ProjectKeyChoices.choices,
                            label="Tonalité",
                            required=False)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super(ProjectUpdateForm, self).__init__(*args, **kwargs)

    def is_valid(self):
        is_valid = super(ProjectUpdateForm, self).is_valid()
        audio_file = self.cleaned_data.get("audio_file")
        if audio_file and not ProjectCreateForm.is_valid_audio_file(
                audio_file
        ):
            self.add_error(
                "audio_file",
                ValidationError("Vous devez choisir un fichier audio")
            )
            is_valid = False
        return is_valid

    def save(self, commit=True):
        project = super(ProjectUpdateForm, self).save(commit)
        audio_file = self.cleaned_data.get("audio_file")
        if audio_file:
            ProjectFile.objects.update_or_create(
                project_file_type=ProjectFileTypeChoices.AUDIO_FILE.name,
                project=project,
                defaults={
                    "file": audio_file,
                    "name": audio_file._name,
                    "uploaded_at": timezone.now()
                }
            )
        return project
