import django_filters
from django import forms
from django.contrib.postgres.search import (
    SearchHeadline,
    SearchQuery,
    SearchRank,
    SearchVector,
)
from django.db.models import F, Value
from django.db.models.functions import Left
from django.db.models.query import EmptyQuerySet
from django.utils.translation import gettext_lazy as _
from django_filters import ModelMultipleChoiceFilter

from general.models import Document, Institution, Language, Project, Subject


class DocumentFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method="ignore", label=_("Search"))

    institution = ModelMultipleChoiceFilter(
        label=_("Institution"),
        queryset=Institution.objects.all().order_by("name"),
        widget=forms.CheckboxSelectMultiple(attrs={"class": "form-check-input"}),
    )
    subjects = ModelMultipleChoiceFilter(
        label=_("Subjects"),
        queryset=Subject.objects.get_used_subjects().order_by("name"),
        widget=forms.CheckboxSelectMultiple(attrs={"class": "form-check-input"}),
    )
    languages = ModelMultipleChoiceFilter(
        label=_("Languages"),
        queryset=Language.objects.all().order_by("name"),
        widget=forms.CheckboxSelectMultiple(attrs={"class": "form-check-input"}),
    )

    class Meta:
        model = Document
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
        # different classes with `.union()`.
        # XXX: Django doesn't order these fields correctly when there is a
        # mixture of model fields and annotations that are not the same for
        # each model. This causes a mismatch of column types, which breaks the
        # `.union()` (or worse, just combines the values of compatible
        # columns). See this bug: https://code.djangoproject.com/ticket/35011
        # We therefore use `F()` even in cases where it shouldn't be needed.
        # An annotation can't share a name with a model field, so anything that
        # occurs on a model needs to be aliased with a different name.
        fields = [
            "id",
            "heading",
            "extra",
            "rank",
            "view",
            "logo_url",
            "associated_url",
        ]

        # In the queries below, any differences between models must be fixed
        # through e.g. `Value` or `F` annotations.
        institution_search_vector = SearchVector("name", weight="A") + SearchVector(
            "abbreviation", weight="A"
        )
        institution_query = Institution.objects.annotate(
            heading=F("name"),
            extra=F("abbreviation"),
            view=Value("institution_detail"),
            logo_url=F("logo"),
            associated_url=F("url"),
            boost=Value(0.02),
            rank=F("boost"),
        )

        for _filter in ("institution", "languages", "subjects"):
            if not isinstance(self.form.cleaned_data[_filter], EmptyQuerySet):
                # We exclude institutions if any filter is active. Not sure
                # what it would mean to filter the institutions by subject,
                # unless our schema changes.
                institution_query = institution_query.none()
                break

        project_search_vector = SearchVector("name", weight="A") + SearchVector(
            "description", weight="B"
        )
        project_query = Project.objects.annotate(
            heading=F("name"),
            extra=F("description"),
            view=Value("project_detail"),
            logo_url=F("logo"),
            associated_url=F("url"),
            boost=Value(0.05),
            rank=F("boost"),
        )

        queryset = super().filter_queryset(queryset)
        project_query = super().filter_queryset(project_query)

        # We limit the headline to limit the performance impact. On very large
        # documents, this slows things down if unconstrained.
        search_headline = SearchHeadline(
            Left("document_data", 20_000), query, max_words=15, min_words=10
        )
        queryset = queryset.annotate(
            heading=F("title"),
            extra=F("description"),
            view=Value("document_detail"),
            logo_url=Value(""),
            associated_url=F("url"),
            boost=Value(0.01),
            rank=F("boost"),
        )
        if search:
            # We only annotate with search related things if needed. The ranking
            # with `SearchRank` and the headling only makes sense if we
            # performed a full-text search. Additionally, an empty search on
            # Project filters out everything, so this is needed for
            # correctness.
            fields.extend(["search_headline"])

            search_rank = SearchRank(F("search_vector"), query, normalization=16)
            queryset = queryset.filter(search_vector=query).annotate(
                rank=search_rank + F("boost"),
                search_headline=search_headline,
            )
            project_query = (
                project_query.annotate(search=project_search_vector)
                .filter(search=query)
                .annotate(
                    search_headline=SearchHeadline(
                        "description", query, max_words=15, min_words=10
                    ),
                    rank=SearchRank(project_search_vector, query, normalization=16) + F("boost"),
                )
            )
            institution_query = (
                institution_query.annotate(search=institution_search_vector)
                .filter(search=query)
                .annotate(
                    search_headline=Value(""),
                    rank=SearchRank(institution_search_vector, query, normalization=16)
                    + F("boost"),
                )
            )

        queryset = queryset.values(*fields)
        project_query = project_query.values(*fields)
        institution_query = institution_query.values(*fields)
        return queryset.union(project_query, institution_query, all=True).order_by(
            "-rank", "heading"
        )

    def ignore(self, queryset, name, value):
        # All fields are handled in `.filter_queryset()`
        return queryset
