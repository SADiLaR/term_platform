from django.shortcuts import render

from general.models import Institution


def institutions_view(request):
    template = "app/institutions.html"

    institutions = Institution.objects.all()
    context = {"institutions_page": "active", "institutions": institutions}

    return render(request, template_name=template, context=context)


def home(request):
    template = "app/home.html"
    context = {"home_page": "active"}

    return render(request, template_name=template, context=context)
