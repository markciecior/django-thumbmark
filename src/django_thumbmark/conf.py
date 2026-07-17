from django.conf import settings


def get_namespace():
    return getattr(settings, "THUMBMARK_NAMESPACE", "django_thumbmark")
