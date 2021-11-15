import os

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import QueryDict
from django.test import TestCase

from app.enums import VALID_AUDIO_FILE_TYPES, ProjectKeyChoices
from app.forms import UserForm, ProjectCreateForm
from app.models import MidUser, Project


class UserCreationFormBaseTestCase(TestCase):
    def setUp(self) -> None:
        self.form_data = {
            "username": "user_test",
            "first_name": "user",
            "last_name": "test",
            "email": "test@test.com",
            "password1": "testpassword00",
            "password2": "testpassword00"
        }


class UserCreationFormTestCase(UserCreationFormBaseTestCase):

    def test_create_user_form_ok(self):
        form = UserForm(data=self.form_data)
        self.assertTrue(form.is_valid())
        # No user should exist yet
        self.assertFalse(MidUser.objects.filter().exists())
        form.save()
        self.assertTrue(MidUser.objects.filter().exists())

    def test_create_user_existing_username(self):
        # Creating a user with same username
        MidUser.objects.create_user(
            username="user_test",
            first_name="lel",
            last_name="lol",
            email="lul@lel.com",
            password="testpassword01"
        )
        form = UserForm(data=self.form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("username", form.errors)

    def test_create_user_existing_email(self):
        # Creating user with same mail
        MidUser.objects.create_user(
            username="oof_man",
            first_name="lel",
            last_name="lol",
            email="test@test.com",
            password="testpassword01"
        )
        form = UserForm(data=self.form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)

    def test_create_user_weak_password(self):
        self.form_data["password1"] = "123"
        self.form_data["password2"] = "123"
        form = UserForm(data=self.form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("password2", form.errors)


class ProjectCreationFormBaseTestCase(TestCase):

    def setUp(self) -> None:
        self.user = MidUser.objects.create_user(
            username="user_test",
            first_name="lel",
            last_name="lol",
            email="lul@lel.com",
            password="testpassword01",
        )
        self.form_data = {
            "name": "test_project",
            "key": ProjectKeyChoices.F.name,
            "tempo": "120"
        }


class ProjectCreationFormTestCases(ProjectCreationFormBaseTestCase):

    def test_create_project_form_ok(self):
        with open(
                os.path.join(
                    settings.BASE_DIR,
                    "app/tests/test_files",
                    "music_test.mp3"), "rb"
        ) as music_file, open(
            os.path.join(
                settings.BASE_DIR,
                "app/tests/test_files",
                "music_sheet.gpx"), "rb"
        ) as music_sheet, open(
            os.path.join(
                settings.BASE_DIR,
                "app/tests/test_files",
                "ableton_project_file.ab"), "rb"
        ) as ableton_file:
            form = ProjectCreateForm(user=self.user,
                                     data=self.form_data,
                                     files={
                                         "audio_file": SimpleUploadedFile(
                                             "test_file.mp3",
                                             music_file.read(),
                                             content_type="audio/mpeg"
                                         ),
                                         "music_sheet": SimpleUploadedFile(
                                             "test_file.gpx",
                                             music_sheet.read(),
                                         ),
                                         "ableton_project_file": SimpleUploadedFile(
                                             "test_file.ab",
                                             ableton_file.read(),
                                         )
                                     })
            self.assertTrue(form.is_valid())
            form.save()
            new_project = Project.objects.get()
            self.assertEqual(new_project.files.count(), 3)

    def test_create_project_form_wrong_audio_file_type(self):
        # Since only audio file is required we don't include
        # music sheet & ableton files
        with open(
                os.path.join(
                    settings.BASE_DIR,
                    "app/tests/test_files",
                    "music_sheet.gpx"), "rb"
        ) as music_file:
            form = ProjectCreateForm(user=self.user,
                                     data=self.form_data,
                                     files={
                                         "audio_file": SimpleUploadedFile(
                                             "test_file.mp3",
                                             music_file.read(),
                                         )
                                     })
            self.assertFalse(form.is_valid())
