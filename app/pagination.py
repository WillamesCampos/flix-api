from rest_framework.pagination import PageNumberPagination


class CustomPageNumberPagination(PageNumberPagination):
    """
    Classe customizada de paginação usando PageNumberPagination.

    Configurações:
    - page_size: 10 registros por página (padrão)
    - page_size_query_param: permite customizar o tamanho da página via query param
    - max_page_size: máximo de 50 registros por página
    """

    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50
