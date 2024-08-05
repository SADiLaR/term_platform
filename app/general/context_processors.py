from django.conf import settings


def template_vars(request):
    return {
        "debug_toolbar": settings.DEBUG and settings.DEBUG_TOOLBAR,
    }
