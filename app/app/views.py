from django.http import HttpResponse
from django.shortcuts import render

from general.models import Institution


def health(request):
    """A very basic (minimal dependency) health endpoint."""
    # If we want/need a health check for DB, cache, files, etc. that should
    # probably be separate.
    return HttpResponse("OK", content_type="text/plain")


def home(request):
    template = "app/home.html"
    context = {"home_page": "active"}

    return render(request, template_name=template, context=context)


def institutions(request):
    template = "app/institutions.html"

    institutions = Institution.objects.all().order_by("name").values()
    context = {"institutions_page": "active", "institutions": institutions}

    return render(request, template_name=template, context=context)


def search(request):
    template = "app/search.html"
    context = {"search_page": "active"}

    return render(request, template_name=template, context=context)


def error_400(request, exception):
    template = "400.html"
    context = {}

    return render(request, template_name=template, context=context)


def error_403(request, exception):
    template = "403.html"
    context = {}

    return render(request, template_name=template, context=context)


def error_404(request, exception):
    template = "404.html"
    context = {}

    return render(request, template_name=template, context=context)


def error_500(request):
    template = "500.html"
    context = {}

    return render(request, template_name=template, context=context)
