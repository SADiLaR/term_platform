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

    institutions = Institution.objects.all()
    context = {"institutions_page": "active", "institutions": institutions}

    return render(request, template_name=template, context=context)
