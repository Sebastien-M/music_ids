import uuid

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from app.enums import VALID_AUDIO_FILE_TYPES, ProjectFileTypeChoices
from app.managers import CustomUserManager


class MidUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True, db_index=True)
    username = models.CharField(error_messages={
        'unique': _('A user with that username already exists.')},
                                help_text=_(
                                    'Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
                                max_length=20, unique=True,
                                validators=[UnicodeUsernameValidator()],
                                verbose_name='username',
                                db_index=True)
    picture = models.FileField(upload_to="profile_pics/", null=True)
    REQUIRED_FIELDS = ["email"]

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Project(models.Model):
    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=6, unique=True, blank=True,
                            db_index=True)
    creator = models.ForeignKey(MidUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(blank=True, null=True)
    modified_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
            self.slug = self.generate_slug()
        self.modified_at = timezone.now()
        return super(Project, self).save(*args, **kwargs)

    @staticmethod
    def generate_slug():
        generated_slug = None
        existing_slug = True
        while existing_slug:
            generated_slug = uuid.uuid4().hex[:6].upper()
            project_instance = Project.objects.filter(slug=generated_slug)
            if not project_instance.exists():
                existing_slug = False
        return generated_slug

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
    project_file_type = models.CharField(max_length=255,
                                         choices=ProjectFileTypeChoices.choices)
    project = models.ForeignKey(Project, on_delete=models.CASCADE,
                                related_name="files")

    def __str__(self):
        return "{} - {}".format(self.name, self.project_file_type)

    def clean(self):
        super(ProjectFile, self).clean()
        if self.project_file_type == ProjectFileTypeChoices.AUDIO_FILE.name:
            if not self.is_valid_audio_file(self.file):
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
    user = models.ForeignKey(MidUser,
                             related_name="favorites",
                             on_delete=models.CASCADE,
                             db_index=True)
    project = models.ForeignKey(Project,
                                on_delete=models.CASCADE,
                                db_index=True)
