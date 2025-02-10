from django.core.paginator import Paginator
from django.db.models import Count, F, Func, OuterRef, Prefetch, Subquery
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.utils.http import urlencode
from django.utils.translation import gettext as _

from general.filters import DocumentFilter
from general.models import Document, Institution, Language, Project, Subject


def health(request):
    """A very basic (minimal dependency) health endpoint."""
    # If we want/need a health check for DB, cache, files, etc. that should
    # probably be separate.
    return HttpResponse("OK", content_type="text/plain")


def home(request):
    template = "app/home.html"
    context = {"current_page": "home"}

    return render(request, template_name=template, context=context)


def about(request):
    template = "app/about.html"
    context = {"current_page": "about"}

    return render(request, template_name=template, context=context)


def legal_notices(request):
    template = "app/legal_notices.html"
    context = {"current_page": "legal_notices"}

    return render(request, template_name=template, context=context)


def get_date_range(project):
    start_date = project.start_date
    end_date = project.end_date

    if start_date and end_date:
        if start_date.year != end_date.year:
            date = f"{start_date.year} – {end_date.year}"
        else:
            date = start_date.year
    elif start_date:
        date = _("Since {year}").format(year=start_date.year)
    elif end_date:
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


def get_languages(languages):
    if languages.count() < 4:
        languages_data = ", ".join(sorted(language.name for language in languages))
    else:
        languages_data = _("Multilingual")
    return languages_data


def get_subjects(subjects):
    if subjects.count() < 4:
        subjects_data = ", ".join(sorted([subject.name for subject in subjects]))
    else:
        subjects_data = _("Multiple subjects")
    return subjects_data


def projects(request):
    template = "app/projects.html"

    projects = (
        Project.objects.select_related("institution")
        .prefetch_related("subjects", "languages")
        .order_by("name")
    )

    if subject_id := request.GET.get("subject"):
        projects = projects.filter(subjects__id=subject_id)
    if language_id := request.GET.get("language"):
        projects = projects.filter(languages__id=language_id)
    if institution_id := request.GET.get("institution"):
        projects = projects.filter(institution__id=institution_id)

    subjects = Subject.objects.get_used_subjects().order_by("name")
    languages = Language.objects.order_by("name")
    institutions = Institution.objects.order_by("name")

    project_data = []
    for project in projects:
        project_subjects = project.subjects.all()
        project_languages = project.languages.all()
        project_data.append(
            {
                "project": project,
                "logo": get_logo(project),
                "subjects": get_subjects(project_subjects),
                "languages": get_languages(project_languages),
                "date": get_date_range(project),
                "institution_name": project.institution.name,
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
        Project.objects.select_related("institution").prefetch_related(
            Prefetch("subjects", queryset=Subject.objects.order_by("name")),
            Prefetch("languages", queryset=Language.objects.order_by("name")),
        ),
        id=project_id,
    )

    context = {
        "current_page": "project_detail",
        "project": project,
        "logo": get_logo(project),
        "subjects": project.subjects.all(),
        "languages": project.languages.all(),
    }
    return render(request, template_name=template, context=context)


def institution_detail(request, institution_id):
    template = "app/institution_detail.html"

    institution = get_object_or_404(Institution, id=institution_id)
    projects = Project.objects.filter(institution=institution).order_by("name")
    documents = Document.objects.filter(institution=institution).order_by("title")

    context = {
        "current_page": "institution_detail",
        "institution": institution,
        "projects": projects,
        "documents": documents,
        "logo": institution.logo,
    }

    return render(request, template_name=template, context=context)


def documents(request):
    template = "app/documents.html"

    documents = (
        Document.objects.select_related("institution")
        .prefetch_related("subjects", "languages")
        .order_by("title")
    )

    url_params = {}
    if subject_id := request.GET.get("subject"):
        documents = documents.filter(subjects__id=subject_id)
        url_params["subject"] = subject_id
    if language_id := request.GET.get("language"):
        documents = documents.filter(languages__id=language_id)
        url_params["language"] = language_id
    if institution_id := request.GET.get("institution"):
        documents = documents.filter(institution__id=institution_id)
        url_params["institution"] = institution_id

    paginator = Paginator(documents, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    subjects = Subject.objects.get_used_subjects().order_by("name")
    languages = Language.objects.order_by("name")
    institutions = Institution.objects.order_by("name")

    document_data = []
    for document in page_obj:
        document_subjects = document.subjects.all()
        document_languages = document.languages.all()
        document_data.append(
            {
                "document": document,
                "subjects": get_subjects(document_subjects),
                "languages": get_languages(document_languages),
                "institution_name": document.institution.name,
                "description": document.description,
                "url": document.url,
                "category": document.document_type,
            }
        )

    context = {
        "current_page": "documents",
        "page_obj": page_obj,
        "documents": document_data,
        "url_params": urlencode(url_params),
        "subjects": subjects,
        "languages": languages,
        "institutions": institutions,
    }
    return render(request, template_name=template, context=context)


def document_detail(request, document_id):
    template = "app/document_detail.html"

    document = get_object_or_404(
        Document.objects.select_related("institution").prefetch_related(
            Prefetch("subjects", queryset=Subject.objects.order_by("name")),
            Prefetch("languages", queryset=Language.objects.order_by("name")),
        ),
        id=document_id,
    )

    context = {
        "current_page": "document_detail",
        "document": document,
    }
    return render(request, template_name=template, context=context)


def languages(request):
    template = "app/languages.html"

    languages = (
        Language.objects.all()
        .prefetch_related(
            Prefetch(
                "document_set",
                queryset=Document.objects.only("id", "title", "languages").order_by("title"),
            ),
            Prefetch(
                "project_set",
                queryset=Project.objects.only("id", "name", "languages").order_by("name"),
            ),
        )
        .order_by("name")
    )

    language_data = []
    for language in languages:
        documents = language.document_set.all()
        projects = language.project_set.all()
        language_data.append(
            {
                "language": language,
                "documents": documents,
                "projects": projects,
            }
        )

    context = {
        "current_page": "languages",
        "language_data": language_data,
    }
    return render(request, template_name=template, context=context)


def subjects(request):
    template = "app/subjects.html"

    subjects = (
        Subject.objects.all()
        .prefetch_related(
            Prefetch(
                "document_set",
                queryset=Document.objects.only("id", "title", "subjects").order_by("title"),
            ),
            Prefetch(
                "project_set",
                queryset=Project.objects.only("id", "name", "subjects").order_by("name"),
            ),
        )
        .order_by("name")
    )

    subject_data = []

    for subject in subjects:
        documents = subject.document_set.all()
        projects = subject.project_set.all()
        if documents or projects:
            subject_data.append(
                {
                    "subject": subject,
                    "documents": documents,
                    "projects": projects,
                }
            )

    paginator = Paginator(subject_data, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "current_page": "subjects",
        "subject_data": page_obj.object_list,
        "page_obj": page_obj,
    }
    return render(request, template_name=template, context=context)


def institutions(request):
    template = "app/institutions.html"
    context = {}

    # https://docs.djangoproject.com/en/stable/topics/db/aggregation/#combining-multiple-aggregations
    subquery = (
        Document.objects.filter(institution=OuterRef("id"))
        .order_by()
        .annotate(count=Func(F("id"), function="Count"))
    )

    institutions = Institution.objects.annotate(
        project_count=Count("project"),
        document_count=Subquery(subquery.values("count")),
    ).order_by("name")

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
        institution_dict["document_count"] = institution.document_count
        institution_dict["id"] = institution.id
        institutions_array.append(institution_dict)

    context = {"current_page": "institutions", "institutions": institutions_array}

    return render(request, template_name=template, context=context)


def search(request):
    f = DocumentFilter(request.GET, queryset=Document.objects.all())

    template = "app/search.html"

    paginator = Paginator(f.qs, 5)  # 5 documents per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    for result in page_obj:
        # Remove headline that is identical to description
        if headline := result.get("search_headline", ""):
            if result["extra"].startswith(headline):
                del result["search_headline"]

    context = {
        "current_page": "search",
        "filter": f,
        "page_obj": page_obj,
        "url_params": pagination_url(request),
    }

    return render(request, template_name=template, context=context)


def pagination_url(request):
    url_params = {
        "search": request.GET.get("search", ""),
        "document_type": request.GET.getlist("document_type", []),
        "institution": request.GET.getlist("institution", []),
        "subjects": request.GET.getlist("subjects", []),
        "languages": request.GET.getlist("languages", []),
    }

    return urlencode(url_params, doseq=True)
