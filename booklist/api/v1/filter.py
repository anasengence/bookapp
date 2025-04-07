from datetime import date
from ...models import Book
from rest_framework import filters
import django_filters


class BookFilter(django_filters.FilterSet):
    published_after = django_filters.DateFilter(
        field_name="date_published", lookup_expr="gte"
    )
    published_before = django_filters.DateFilter(
        field_name="date_published", lookup_expr="lte"
    )

    class Meta:
        model = Book
        fields = ["published_after", "published_before"]


class CustomFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        this_year = request.query_params.get("this_year", False)
        if this_year and this_year.lower() == "true":
            queryset = queryset.filter(date_published__year=(date.today().year) - 1)

        return queryset
