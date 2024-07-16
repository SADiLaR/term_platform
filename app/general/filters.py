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
from django_filters import ModelMultipleChoiceFilter, MultipleChoiceFilter

from general.models import DocumentFile, Institution, Language, Project, Subject


class DocumentFileFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method="filter_search", label="Search")

    institution = ModelMultipleChoiceFilter(
        queryset=Institution.objects.all(), widget=forms.CheckboxSelectMultiple
    )
    document_type = MultipleChoiceFilter(
        choices=DocumentFile.document_type_choices, widget=forms.CheckboxSelectMultiple
    )
    subjects = ModelMultipleChoiceFilter(
        queryset=Subject.objects.all(), widget=forms.CheckboxSelectMultiple
    )
    languages = ModelMultipleChoiceFilter(
        queryset=Language.objects.all(), widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = DocumentFile
        fields = [
            "document_type",
            "institution",
            "subjects",
            "languages",
        ]

    def filter_queryset(self, queryset):
        # More information about weighting and normalization in postgres:
        # https://www.postgresql.org/docs/current/textsearch-controls.html#TEXTSEARCH-RANKING
        queryset = super().filter_queryset(queryset)

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
            "logo_url",
        )

        # In the queries below, any differences between models must be fixed
        # through e.g. `Value` or `F` annotations.
        project_search_vector = SearchVector("name", weight="A") + SearchVector(
            "description", weight="B"
        )
        project_query = (
            Project.objects.annotate(
                heading=F("name"),
                view=Value("project_detail"),
                logo_url=F("logo"),
                search_headline=SearchHeadline("description", query),
                rank=SearchRank(project_search_vector, query, normalization=16),
                search=project_search_vector,
            )
            .filter(search=query)
            .values(*fields)
        )

        # We limit the headline to limit the performance impact. On very large
        # documents, this slows things down if unconstrained.
        search_headline = SearchHeadline(Left("document_data", 200_000), query)
        search_rank = SearchRank(F("search_vector"), query, normalization=16)
        queryset = queryset.annotate(
            heading=F("title"),
            view=Value("document_detail"),
            logo_url=Value("no_logo"),
            rank=search_rank,
            search_headline=search_headline,
        ).values(*fields)
        return queryset.union(project_query).order_by("-rank")

    def filter_search(self, queryset, name, value):
        if value:
            query = SearchQuery(value.strip())
            return queryset.filter(search_vector=query)

        else:
            return queryset
