from django.http import HttpResponse
from django.shortcuts import render


def health(request):
    """A very basic (minimal dependency) health endpoint."""
    # If we want/need a health check for DB, cache, files, etc. that should
    # probably be separate.
    return HttpResponse("OK", content_type="text/plain")


def home(request):
    template = "app/home.html"
    context = {}

    return render(request, template_name=template, context=context)


def error_page(request):
    template = "app/error_page.html"
    context = {}

    return render(request, template_name=template, context=context)
