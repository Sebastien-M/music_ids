from django import forms
from django.contrib.auth.forms import UserCreationForm, UsernameField

from app.models import MidUser


class UserForm(UserCreationForm):
    class Meta:
        model = MidUser
        field_classes = {'username': UsernameField}
        fields = ("username", "first_name", "last_name", "email", "password1", "password2")

    def is_valid(self):
        return super(UserForm, self).is_valid()
