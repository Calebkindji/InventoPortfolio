from rest_framework.pagination import PageNumberPagination


class ExplorePagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'limit'
    page_query_param = 'page'
    max_page_size = 50
