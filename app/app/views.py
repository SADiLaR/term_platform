from django.core.paginator import Paginator
from django.shortcuts import render

from general.models import Institution


def institutions_view(request):
    template = "app/institutions.html"

    paginator = Paginator(Institution.objects.all(), 5)
    page_number = request.GET.get("page")
    institutions = paginator.get_page(page_number)

    context = {"institutions": institutions}

    return render(request, template_name=template, context=context)


def home(request):
    template = "app/home.html"
    context = {}

    return render(request, template_name=template, context=context)
