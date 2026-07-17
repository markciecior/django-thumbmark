# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3] - 2026-07-17

### Added

- A `unittest`-based test suite (runnable via `python manage.py test`), covering `DjTmScriptView`, `DjTmLoginView`, and `login_required_thumbmark`. A `test.yml` GitHub Actions workflow runs it across the supported Python/Django matrix on every push/PR, and the release workflow (`publish.yml`) now runs it as a required step before publishing to PyPI.

### Security

- The `tm` endpoint now requires a `POST` request with a valid CSRF token instead of `GET`. Previously, an unauthenticated `GET` to `tm/?tmid=<value>` would log in (creating the account if needed) using the attacker-controlled `tmid` as the username, with no CSRF protection — allowing a third-party page to force-login a visitor into an arbitrary or attacker-chosen account. **Breaking change** for any downstream project that called the `tm` endpoint directly via `GET`; the documented integration (the bundled `login.html`/`base.html`) is unaffected.

### Changed

- The login page (`login.html`) now shows a "Signing you in…" message instead of a blank page while the fingerprint is computed and submitted.
- Relicensed from GPL-3.0-or-later to MIT, matching the license of the [ThumbmarkJS](https://github.com/thumbmarkjs/thumbmarkjs) library this project wraps. The `pyproject.toml` `license`/classifier and the `LICENSE` file previously disagreed (GPL text vs. a BSD classifier); both now consistently say MIT.
- The bundled ThumbmarkJS CDN script tag is now pinned to a specific version (`@1.10.0`) instead of resolving to whatever is currently latest on jsDelivr.
- Migrated from the deprecated `ThumbmarkJS.getFingerprint()` global function to the current `new ThumbmarkJS.Thumbmark().get()` class-based API; the fingerprint hash is now read from `res.thumbmark`.
- Added `pip install` instructions to the README (previously undocumented in this changelog).
- `django_thumbmark.__version__` is now set (read from installed package metadata via `importlib.metadata`, so it can't drift from `pyproject.toml`'s version).
- `login_required_thumbmark` and `DjTmLoginView` now locate the `tm`/`tmlogin` views via a fixed URL namespace (`django_thumbmark` by default, configurable with the new `THUMBMARK_NAMESPACE` setting) instead of the namespace of whichever view triggered the redirect. This means `django_thumbmark.urls` can now be `include()`d normally like any other reusable app, and protected views no longer need to live in the same namespace as the `tm`/`tmlogin` URLs. **Breaking change**: if you previously copied the `tm`/`tmlogin` paths directly into an app-specific `urls.py` without an `app_name` matching `django_thumbmark`, set `THUMBMARK_NAMESPACE` to whatever namespace that `urls.py` is included under (or add `app_name = "django_thumbmark"` to it).

## [0.2] - 2024-11-21

### Added

### Changed

- Updated README to show only importing views within an existing app

### Removed

## [0.1] - 2024-11-20

### Added

- Initial release

### Fixed


### Changed


### Removed
