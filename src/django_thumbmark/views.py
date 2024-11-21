from django.http import JsonResponse
from django.contrib.auth import get_user_model, login
from django.urls import reverse, resolve
from django.views import View
from django.views.generic import TemplateView


class DjTmScriptView(View):
    def get(self, request):
        next = request.session.get("next")
        if not request.user.is_authenticated:
            tmid = request.GET.get("tmid")
            user = self.get_user_object(request, tmid=tmid)
            login(request, user)
        return JsonResponse({"url": next})

    def get_user_object(self, request, *args, **kwargs):
        tmid = kwargs["tmid"]
        UserModel = get_user_model()
        user, _ = UserModel.objects.get_or_create(
            username=self.get_username(request, tmid=tmid),
            defaults={
                "username": self.get_username(request, tmid=tmid),
                "first_name": self.get_first_name(request),
                "last_name": self.get_last_name(request),
            },
        )
        return user

    def get_username(self, request, *args, **kwargs):
        u = kwargs["tmid"]
        return u

    def get_first_name(self, request, *args, **kwargs):
        return "Test"

    def get_last_name(self, request, *args, **kwargs):
        return "User"


class DjTmLoginView(TemplateView):
    template_name = "django_thumbmark/login.html"

    def get(self, request, *args, **kwargs):
        next = request.GET.get("next")
        request.session["next"] = next
        kwargs["path"] = request.path
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        path = kwargs["path"]
        context["tm_url"] = reverse(f"{resolve(path).namespace}:tm")
        return context
