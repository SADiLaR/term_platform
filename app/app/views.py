import os

from django.contrib.postgres.search import SearchHeadline, SearchQuery, SearchRank
from django.core.paginator import Paginator
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.utils.translation import gettext as _

from general.models import DocumentFile, Institution, Language, Project, Subject


def health(request):
    """A very basic (minimal dependency) health endpoint."""
    # If we want/need a health check for DB, cache, files, etc. that should
    # probably be separate.
    return HttpResponse("OK", content_type="text/plain")


def home(request):
    template = "app/home.html"
    context = {"current_page": "home"}

    return render(request, template_name=template, context=context)


def get_date_range(project):
    start_date = project.start_date
    end_date = project.end_date

    if (start_date is not None) and (end_date is not None) and (start_date.year != end_date.year):
        date = f"{start_date.year} – {end_date.year}"
    elif (start_date is not None) and (end_date is not None) and (start_date.year == end_date.year):
        date = start_date.year
    elif start_date is not None:
        date = _("Since {year}").format(year=start_date.year)
    elif end_date is not None:
        date = _("Until {year}").format(year=end_date.year)
    else:
        date = None
    return date


def get_logo(project):
    if project.logo:
        logo = project.logo
    elif project.institution.logo:
        logo = project.institution.logo
    else:
        logo = None
    return logo


def projects(request):
    template = "app/projects.html"

    subject_id = request.GET.get("subject")
    language_id = request.GET.get("language")
    institution_id = request.GET.get("institution")

    projects = (
        Project.objects.select_related("institution")
        .prefetch_related("subjects", "languages")
        .order_by("name")
    )

    if subject_id:
        projects = projects.filter(subjects__id=subject_id)
    if language_id:
        projects = projects.filter(languages__id=language_id)
    if institution_id:
        projects = projects.filter(institution__id=institution_id)

    subjects = Subject.objects.order_by("name")
    languages = Language.objects.order_by("name")
    institutions = Institution.objects.order_by("name")

    project_data = []
    for project in projects:
        project_subjects = project.subjects.all()
        project_languages = project.languages.all()

        if project_languages.count() < 4:
            languages_data = ", ".join(sorted(language.name for language in project_languages))
        else:
            languages_data = _("Multilingual")

        if project_subjects.count() < 4:
            subjects_data = ", ".join(sorted([subject.name for subject in project_subjects]))
        else:
            subjects_data = _("Multiple subjects")

        logo = get_logo(project)

        institution_name = project.institution.name

        date = get_date_range(project)

        project_data.append(
            {
                "project": project,
                "logo": logo,
                "subjects": subjects_data,
                "languages": languages_data,
                "date": date,
                "institution_name": institution_name,
                "description": project.description,
            }
        )

    context = {
        "current_page": "projects",
        "projects": project_data,
        "subjects": subjects,
        "languages": languages,
        "institutions": institutions,
    }

    return render(request, template_name=template, context=context)


def project_detail(request, project_id):
    template = "app/project_detail.html"

    project = get_object_or_404(
        Project.objects.select_related("institution").prefetch_related("subjects", "languages"),
        id=project_id,
    )

    logo = get_logo(project)

    context = {
        "current_page": "project_detail",
        "project": project,
        "logo": logo,
        "subjects": project.subjects.all(),
        "languages": project.languages.all(),
    }
    return render(request, template_name=template, context=context)


def institution_detail(request, institution_id):
    template = "app/institution_detail.html"

    institution = get_object_or_404(Institution, id=institution_id)
    projects = Project.objects.filter(institution=institution)
    documents = DocumentFile.objects.filter(institution=institution)

    logo = institution.logo

    context = {
        "current_page": "institution_detail",
        "institution": institution,
        "projects": projects,
        "documents": documents,
        "logo": logo,
    }

    return render(request, template_name=template, context=context)


def document_detail(request, project_id):
    template = "app/document_detail.html"

    document = DocumentFile.objects.get(id=document_id)

    context = {
        "current_page": "document_detail",
    }
    return render(request, template_name=template, context=context)


def language_detail(request, project_id):
    template = "app/language_detail.html"

    project = Project.objects.get(id=project_id)

    context = {
        "current_page": "language_detail",
    }
    return render(request, template_name=template, context=context)


def subject_detail(request, project_id):
    template = "app/subject_detail.html"

    project = Project.objects.get(id=project_id)

    context = {
        "current_page": "subject_detail",
        "project": project,
    }
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
        institution_dict["id"] = institution.id
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
