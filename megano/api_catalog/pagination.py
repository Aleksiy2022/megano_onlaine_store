from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class MyPaginationClass(PageNumberPagination):
    page_size = 5
    page_query_param = 'currentPage'
    max_page_size = 5
    def get_paginated_response(self, data):
        return Response({
            'items': data,
            'currentPage': self.page.number,
            'lastPage': self.page.paginator.num_pages,
        })
