from django.http import HttpResponse
from django.urls import include, path

from django_thumbmark.decorators import login_required_thumbmark


@login_required_thumbmark
def protected_view(request):
    return HttpResponse("protected content")


urlpatterns = [
    path("", include("django_thumbmark.urls", namespace="custom-thumbmark")),
    path("protected/", protected_view, name="protected"),
]
