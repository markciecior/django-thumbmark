from django.http import HttpResponse
from django.urls import path

from django_thumbmark.decorators import login_required_thumbmark
from django_thumbmark.views import DjTmLoginView, DjTmScriptView

app_name = "tests"


@login_required_thumbmark
def protected_view(request):
    return HttpResponse("protected content")


urlpatterns = [
    path("tm/", DjTmScriptView.as_view(), name="tm"),
    path("login/", DjTmLoginView.as_view(), name="tmlogin"),
    path("protected/", protected_view, name="protected"),
]
