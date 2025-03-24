from django_filters import rest_framework as filters
from ..models import Book


class BookFilter(filters.FilterSet):
    published_after = filters.DateFilter(field_name='date_published', lookup_expr='gte')
    published_before = filters.DateFilter(field_name='date_published', lookup_expr='lte')
    class Meta:
        model = Book
        fields = ['published_after', 'published_before']