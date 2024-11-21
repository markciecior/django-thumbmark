from django_thumbmark.views import DjTmScriptView, DjTmLoginView
from django.urls import path


app_name = "django_thumbmark"
urlpatterns = [
    path("tm/", DjTmScriptView.as_view(), name="tm"),
    path("login/", DjTmLoginView.as_view(), name="tmlogin"),
]
