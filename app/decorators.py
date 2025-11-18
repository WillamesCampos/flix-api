from functools import wraps

from app.settings import logger


def log_request(func):
    """
    Decorator para logar requisições em views do DRF.

    Captura informações da requisição (user, path, method, content_type)
    e registra no logger antes de executar o método.

    Uso:
        @log_request
        def list(self, request, *args, **kwargs):
            return super().list(request, *args, **kwargs)
    """

    @wraps(func)
    def wrapper(self, request, *args, **kwargs):
        logger_data = {
            'user': request.user.email if request.user.is_authenticated else 'anonymous',
            'path': request.path,
            'method': request.method,
            'content_type': request.content_type,
        }
        logger.info(logger_data)
        return func(self, request, *args, **kwargs)

    return wrapper
