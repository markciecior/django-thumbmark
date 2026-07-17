from django.urls import include, path

urlpatterns = [
    path("", include("tests.app_urls")),
]
