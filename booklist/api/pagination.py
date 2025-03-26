from rest_framework.pagination import (
    PageNumberPagination,
    LimitOffsetPagination,
    CursorPagination,
)
from rest_framework.response import Response


class CustomLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 2
    # max_limit = 10


class CustomPageNumberPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = "page_size"
    # page_query_param = 'page_nomber'
    # max_page_size = 5
    
    

    def get_paginated_response(self, data):
        return Response(
            {
                "metadata": {
                    "total_items": self.page.paginator.count,
                    "total_pages": self.page.paginator.num_pages,
                    "current_page": self.page.number,
                    "page_size": self.get_page_size(self.request),
                    "next_page": self.get_next_link(),
                    "previous_page": self.get_previous_link(),
                },
                "results": data,
            }
        )


class CustomCursorPagination(CursorPagination):
    page_size = 2
    ordering = "date_published"
    cursor_query_param = "cursor"
    # max_page_size = 5
