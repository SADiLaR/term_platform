import django_filters
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector

from general.models import DocumentFile


class DocumentFileFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method="filter_search", label="Search")

    class Meta:
        model = DocumentFile
        fields = [
            "document_type",
            "institution",
            "subjects",
            "languages",
        ]

    def filter_search(self, queryset, name, value):
        if value:
            queue = SearchQuery(value)
            search_vector = SearchVector("title", "description", "document_data")
            # search_vector = SearchVector('document_data')
            search_rank = SearchRank(search_vector, queue)
            queryset = (
                queryset.annotate(
                    rank=search_rank,
                    search_vector_annotation=search_vector,  # Renamed annotation to avoid conflict
                )
                .select_related("institution")
                .filter(search_vector_annotation=queue)
                .order_by("-rank")
            )
        return queryset
