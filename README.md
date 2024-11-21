# django-thumbmark
&nbsp;[![License](https://img.shields.io/pypi/l/django-thumbmark.svg?label=License)](https://pypi.python.org/pypi/django-thumbmark)&nbsp;[![python versions](https://img.shields.io/pypi/pyversions/django-thumbmark.svg?label=python%20versions)](https://pypi.python.org/pypi/django-thumbmark)&nbsp;[![PyPI version](https://img.shields.io/pypi/v/django-thumbmark.svg?label=PyPI%20version)](https://pypi.python.org/pypi/django-thumbmark)

Django app to transparently identify users with the [ThumbmarkJS](https://github.com/thumbmarkjs/thumbmarkjs) library.

This app includes a decorator that mimics the built-in ```login_required``` decorator provided by Django.  Views using this decorator will have unidentified users transparently redirected through a page where the [ThumbmarkJS](https://github.com/thumbmarkjs/thumbmarkjs) library is used to generate a unique identifier for the client.  This unique identifier is then mapped to a Django user and associated with the ```HttpRequest``` object.

Common use cases include public forms that should be limited to one submission per user, without requring a username/password login.
* Survey Submissions
* Feedback Forms
* Anonymous Polls

## Usage

Add the included decorator to your function- or class-based view:

```python
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator

from django_thumbmark.decorators import login_required_thumbmark

@login_required_thumbmark
def my_function_based_view(request):
    # ...
    print(request.user) # <-- The User attribute will be populated

### --- or --- ###

@method_decorator(login_required_thumbmark, name='dispatch')
class MyClassBasedView(TemplateView):
    # ...
    def get(self, request):
        print(request.user) # <-- The User attribute will be populated
```

## Standard Installation

Install from PyPi:

```python
python -m pip install django-thumbmark
```

Add `django_thumbmark` to your `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    # ...
    'django_thumbmark',
]
```

To use the app as written (without customization) add these two views in your app's ```urls.py``` file.

> [!IMPORTANT]
> The names of these two URLs __must__ be ```tm``` and ```tmlogin``` as shown.

```python
# myapp/urls.py
from django_thumbmark.views import DjTmLoginView, DjTmScriptView

urlpatterns = [
    # ...
    path("tm/", DjTmScriptView.as_view(), name="tm"),
    path("login/", DjTmLoginView.as_view(), name="tmlogin"),
]
```

## Installation with Customizations

To use the app with customization, overwrite the included DjTmScriptView as needed.  Then add this modified DjTmScriptView *and* the included DjTmLoginView to your app-specific ```urls.py``` file.

> [!IMPORTANT]
> The names of these two URLs in your app-specific ```urls.py``` file __must__ be ```tm``` and ```tmlogin``` as shown.

```python
# myapp/views.py
from django_thumbmark.views import DjTmScriptView
from django.utils import timezone # ... as an example of customized usage

    # ...
    class MyDjTmScriptView(DjTmScriptView):
        def get_first_name(self, request, *args, **kwargs):
            return "CustomFirstName"

        def get_username(self, request, *args, **kwargs):
            tmid = kwargs["tmid"]
            path = request.path
            time = timezone.now().strftime("%Y-%m-%dT%H:%M:%S")
            return f"{tmid}-{path}-{time}"


# myapp/urls.py
from myapp import views
from django_thumbmark.views import DjTmLoginView

urlpatterns = [
    # ...
    path("tm/", views.MyDjTmScriptView.as_view(), name="tm"), # The URL name is "tm"
    path("login/", DjTmLoginView.as_view(), name="tmlogin"), # The URL name is "tmlogin"
]
```

To modify the included HTML template, overwrite the ```django_thumbmark/login.html``` template within your app's templates directory.

```.
├── manage.py
├── project_root
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── requirements.txt
└── myapp
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── forms.py
    ├── migrations
    │   ├── 0001_initial.py
    ├── models.py
    ├── templates
    │   ├── django_thumbmark ## Create this directory
    │   │   └── login.html   ## Add this file
    │   └── myapp
    │       ├── index.html
    │       └── success.html
    ├── tests.py
    ├── urls.py
    └── views.py
```

The options with which this overwritten template file can be modified are shown in the Customization section below.

## Details

When a view uses this decorator
1) If the user is already authenticated, nothing happens.
2) If the user hasn't been authenticated they are redirected to a new login page named ```tmlogin```.  This login page contains the [ThumbmarkJS](https://github.com/thumbmarkjs/thumbmarkjs) script to generate a unique ID.
3) The unique ID is sent by Javascript via a GET request to a second view named ```tm```.
4) The second view uses the unique ID to search for an existing User object.  A new User object is created if no object is found.
5) The user is logged in and associated with the request.
6) The user is redirected back to their original page.


## Customization

### New User First/Last Names

By default, if a new User object is created, the first and last names are set to "Test" and "User," respectively.  These can be modified by overwriting the ```DjTmScriptView.get_first_name()``` and ```DjTmScriptView.get_last_name()``` functions.

### New User Username

By default, if a new User object is created, the username is set to the unique ID generated by [ThumbmarkJS](https://github.com/thumbmarkjs/thumbmarkjs).  This can be modified by overwriting the ```DjTmScriptView.get_username()``` function.

### New User Object

By default, Django's ```get_or_create()``` function is used to find/create a User object directly, which is then logged in and associated with the request.  To modify how that user is discovered and/or created, you can overwrite the ```DjTmScriptView.get_user_object_()``` function.

### JavaScript Disabled Output

By default, if the browser doesn't have JavaScript enabled, a static text string will be shown to the user instructing them to enable Javascript to use this site.  This text can be changed by overwriting the ```django_thumbprint/login.html``` template and modifying this block:

```html
{% block no-js-message %}Please, pretty please, won't you enable JavaScript?{% endblock %}
```

### ThumbmarkJS Source

By default the [ThumbmarkJS](https://github.com/thumbmarkjs/thumbmarkjs) library is loaded from cdn.jsdelivr.net.  This can be changed (to reference a static, self-hosted copy or similar) by overwriting the ```django_thumbprint/login.html``` template and modifying this block:

```html
{% block js-source %}<script src="https://cdn.jsdelivr.net/npm/@thumbmarkjs/thumbmarkjs/dist/thumbmark.umd.js"></script>{% endblock %}
```

### ThumbmarkJS Script

By default the [ThumbmarkJS](https://github.com/thumbmarkjs/thumbmarkjs) script is run using [this example](https://github.com/thumbmarkjs/thumbmarkjs?tab=readme-ov-file#and-on-the-web-page) from its homepage.  The contents of that script can be changed by overwriting the ```django_thumbprint/login.html template``` and modifying this block:

```html
{% block js-script %}<script>console.log('This is my new script')</script>{% endblock %}
```

> [!IMPORTANT]
> Take extreme caution when modifying this template block to ensure dynamic values are properly escaped.

## Versioning

This package uses [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
TL;DR you are safe to use [compatible release version specifier](https://packaging.python.org/en/latest/specifications/version-specifiers/#compatible-release) `~=MAJOR.MINOR` in your `pyproject.toml` or `requirements.txt`.

## Release process

```python
python -m pip install build
python -m pip install twine
python -m build
python -m twine upload dist/*
```
