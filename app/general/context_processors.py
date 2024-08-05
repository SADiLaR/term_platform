from django.conf import settings


def template_vars(request):
    return {
        "debug_toolbar": settings.DEBUG and settings.DEBUG_TOOLBAR,
        "BASE_TEMPLATE": "base_htmx.html" if request.htmx else "base.html",
    }
