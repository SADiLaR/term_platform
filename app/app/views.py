from django.shortcuts import render


def home(request):
    template = "app/home.html"
    context = {}

    return render(request, template_name=template, context=context)
