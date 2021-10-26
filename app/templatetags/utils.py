from django import template

from app.models import FavoriteProject

register = template.Library()


@register.simple_tag
def is_favorite(user, project):
    return FavoriteProject.objects.filter(user=user, project=project).exists()
