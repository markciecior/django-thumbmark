from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("django-thumbmark")
except PackageNotFoundError:
    __version__ = "unknown"
