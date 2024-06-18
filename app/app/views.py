import os

from django.contrib.postgres.search import SearchHeadline, SearchQuery, SearchRank
from django.core.paginator import Paginator
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render

from general.models import DocumentFile, Institution


def health(request):
    """A very basic (minimal dependency) health endpoint."""
    # If we want/need a health check for DB, cache, files, etc. that should
    # probably be separate.
    return HttpResponse("OK", content_type="text/plain")


def home(request):
    template = "app/home.html"
    context = {"current_page": "home"}

    return render(request, template_name=template, context=context)


def institutions(request):
    template = "app/institutions.html"
    context = {}

    institutions = Institution.objects.annotate(project_count=Count("project")).order_by("name")

    institutions_array = []

    for institution in institutions:
        institution_dict = {
            "name": institution.name,
            "abbreviation": institution.abbreviation,
            "url": institution.url,
            "email": institution.email,
            "logo": institution.logo,
        }
        completed_fields_count = sum(1 for value in institution_dict.values() if value)

        """Rating returns % number of completed fields.

        Profile completion weighting is % number of completed fields in 5 star rating.

        Profile completion is calculated using the number of present model fields,
        model fields have to be added to the institution_dict"""

        rating = (completed_fields_count / len(institution_dict)) * 100
        institution_dict["rating"] = round(rating)
        institution_dict["project_count"] = institution.project_count
        institutions_array.append(institution_dict)

    context = {"current_page": "institutions", "institutions": institutions_array}

    return render(request, template_name=template, context=context)


def search(request):
    q = request.GET.get("q")

    if q:
        queue = SearchQuery(q)
        search_headline = SearchHeadline("document_data", queue)

        documents = (
            DocumentFile.objects.annotate(rank=SearchRank("search_vector", queue))
            .annotate(search_headline=search_headline)
            .filter(search_vector=queue)
            .order_by("-rank")
        )

    else:
        documents = None

    # Create a Paginator instance with the documents and the number of items per page
    paginator = Paginator(documents, 10) if documents else None  # Show 10 documents per page

    # Get the page number from the request's GET parameters
    page_number = request.GET.get("page")

    # Use the get_page method to get the Page object for that page number
    page_obj = paginator.get_page(page_number) if paginator else None

    feature_flag = os.getenv("FEATURE_FLAG", False)

    template = "app/search.html"
    context = {
        "documents": page_obj,
        "current_page": "search",
        "document_count": len(documents) if documents else 0,
        "feature_flag": feature_flag,
    }

    return render(request, template_name=template, context=context)
