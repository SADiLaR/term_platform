import django_filters
from django import forms
from django.contrib.postgres.search import SearchHeadline, SearchQuery, SearchRank
from django.db.models import F
from django_filters import ModelMultipleChoiceFilter, MultipleChoiceFilter

from general.models import DocumentFile, Institution, Language, Subject


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
        queryset = super().filter_queryset(queryset)

        search = self.form.cleaned_data.get("search", "")
        queue = SearchQuery(search.strip())
        search_rank = SearchRank(F("search_vector"), queue)
        search_headline = SearchHeadline("document_data", queue)
        queryset = (
            queryset.annotate(
                rank=search_rank,
                search_headline=search_headline,
            )
            .defer("document_data")
            .select_related("institution")
        ).order_by("-rank")

        return queryset

    def filter_search(self, queryset, name, value):
        if value:
            queue = SearchQuery(value.strip())
            return queryset.filter(search_vector=queue)

        else:
            return queryset
