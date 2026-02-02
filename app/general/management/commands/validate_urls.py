import ssl
import sys
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen

from django.conf import settings
from django.core.management.base import BaseCommand
from django.urls import reverse

from general.models import Document, Institution, Project


class Command(BaseCommand):
    help = "Validate stored URLs for Projects, Documents and Institutions."

    def handle(self, *args, **options):
        failures = []
        total_checked = 0

        for project in Project.objects.all():
            total_checked += self._check_record(project, "Project", failures)

        for institution in Institution.objects.all():
            total_checked += self._check_record(institution, "Institution", failures)

        for document in Document.objects.all():
            total_checked += self._check_record(document, "Document", failures)

        if failures:
            for failure in failures:
                print(failure)
            print(f"Failures: {len(failures)} of {total_checked} URLs failed.")
            sys.exit(1)

        print(f"All URLs are reachable (checked {total_checked} URLs).")
        sys.exit(0)

    def _check_record(self, instance, model_name, failures):
        url_value = getattr(instance, "url", "")
        if not url_value:
            return 0

        success, reason = self._check_url(url_value)
        if not success:
            # Document uses 'title', others use 'name'
            display_name = getattr(instance, "title", None) or getattr(instance, "name", "")
            admin_url = self._build_admin_url(instance)
            failures.append(
                f'{model_name} id={instance.pk} name="{display_name}": {url_value} -> {reason} (admin: {admin_url})'
            )
        return 1

    def _check_url(self, url):
        parsed = urlparse(url)
        if parsed.scheme not in {"http", "https"}:
            return False, "Invalid scheme"

        head_ok, head_reason = self._request(url, method="HEAD")
        if head_ok:
            return True, ""

        if head_reason in {"HTTP 400", "HTTP 403", "HTTP 405"}:
            get_ok, get_reason = self._request(url, method="GET")
            if get_ok:
                return True, ""
            return False, get_reason

        return False, head_reason

    def _request(self, url, method):
        try:
            context = ssl._create_unverified_context()
            req = Request(url=url, method=method, headers={"User-Agent": "url-validator/1.0"})
            with urlopen(req, timeout=15, context=context) as resp:
                status = getattr(resp, "status", None) or resp.getcode()
                if 200 <= status < 400:
                    return True, ""
                return False, f"HTTP {status}"
        except HTTPError as exc:
            return False, f"HTTP {exc.code}"
        except URLError as exc:
            return False, self._format_url_error(exc)
        except Exception as exc:  # noqa: BLE001 - catch unexpected errors (timeout, etc.) to prevent command crash
            return False, f"Error: {exc}"

    def _format_url_error(self, exc):
        reason = getattr(exc, "reason", None)
        if reason:
            return str(reason)
        return str(exc)

    def _build_admin_url(self, instance):
        """Build the admin change URL for the instance.
        If CSRF_TRUSTED_ORIGINS is configured, return full URL; otherwise return relative path."""
        path = reverse(
            f"admin:{instance._meta.app_label}_{instance._meta.model_name}_change",
            args=[instance.pk],
        )

        if settings.CSRF_TRUSTED_ORIGINS:
            base = settings.CSRF_TRUSTED_ORIGINS[0].rstrip("/") + "/"
            return urljoin(base, path)

        return path
