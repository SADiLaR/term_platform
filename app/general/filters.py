import django_filters
from django import forms
from django.contrib.postgres.search import (
    SearchHeadline,
    SearchQuery,
    SearchRank,
    SearchVector,
)
from django.db.models import F, Value
from django.db.models.functions import Greatest, Left
from django.utils.translation import gettext_lazy as _
from django_filters import ModelMultipleChoiceFilter, MultipleChoiceFilter

from general.models import DocumentFile, Institution, Language, Project, Subject


class DocumentFileFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method="ignore", label=_("Search"))

    institution = ModelMultipleChoiceFilter(
        label=_("Institution"),
        queryset=Institution.objects.all().order_by("name"),
        widget=forms.CheckboxSelectMultiple(attrs={"class": "form-check-input"}),
    )
    subjects = ModelMultipleChoiceFilter(
        label=_("Subjects"),
        queryset=Subject.objects.all().order_by("name"),
        widget=forms.CheckboxSelectMultiple(attrs={"class": "form-check-input"}),
    )
    languages = ModelMultipleChoiceFilter(
        label=_("Languages"),
        queryset=Language.objects.all().order_by("name"),
        widget=forms.CheckboxSelectMultiple(attrs={"class": "form-check-input"}),
    )

    class Meta:
        model = DocumentFile
        fields = [
            "institution",
            "subjects",
            "languages",
        ]

    def filter_queryset(self, queryset):
        # More information about weighting and normalization in postgres:
        # https://www.postgresql.org/docs/current/textsearch-controls.html#TEXTSEARCH-RANKING

        search = self.form.cleaned_data.get("search", "").strip()
        query = SearchQuery(search)

        # A fixed list of identical fields are required to join queries of
        # different classes with `.union()`:
        fields = (
            "id",
            "heading",
            "description",
            "rank",
            "search_headline",
            "view",
            "logo_url",
            "associated_url",
        )

        # In the queries below, any differences between models must be fixed
        # through e.g. `Value` or `F` annotations.
        project_search_vector = SearchVector("name", weight="A") + SearchVector(
            "description", weight="B"
        )
        project_query = Project.objects.annotate(
            heading=F("name"),
            view=Value("project_detail"),
            logo_url=F("logo"),
            associated_url=F("url"),
            search_headline=SearchHeadline("description", query, max_words=15, min_words=10),
            rank=SearchRank(project_search_vector, query, normalization=16),
        )

        queryset = super().filter_queryset(queryset)
        project_query = super().filter_queryset(project_query)

        # We limit the headline to limit the performance impact. On very large
        # documents, this slows things down if unconstrained.
        search_headline = SearchHeadline(
            Left("document_data", 20_000), query, max_words=15, min_words=10
        )
        search_rank = SearchRank(F("search_vector"), query, normalization=16)
        queryset = queryset.annotate(
            heading=F("title"),
            view=Value("document_detail"),
            logo_url=Value(""),
            associated_url=F("url"),
            rank=search_rank,
            search_headline=search_headline,
        )
        if search:
            # An empty search on Project filters out everything.
            queryset = queryset.filter(search_vector=query)
            project_query = project_query.annotate(search=project_search_vector).filter(
                search=query
            )

        queryset = queryset.values(*fields)
        project_query = project_query.values(*fields)
        return queryset.union(project_query, all=True).order_by("-rank")

    def ignore(self, queryset, name, value):
        # All fields are handled in `.filter_queryset()`
        return queryset
