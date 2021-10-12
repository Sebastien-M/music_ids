from django.conf import settings


def version_processor(request):
    version = settings.VERSION
    return {'version': version}