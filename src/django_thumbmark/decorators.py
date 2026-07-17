from django.http import HttpResponseRedirect
from django.urls import reverse

from django_thumbmark.conf import get_namespace


def login_required_thumbmark(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(
                f"{reverse(f'{get_namespace()}:tmlogin')}?next={request.path}"
            )
        response = view_func(request, *args, **kwargs)
        return response

    return wrapper
