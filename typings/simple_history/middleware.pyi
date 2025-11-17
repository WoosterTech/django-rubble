

from django.utils.decorators import sync_and_async_middleware

@sync_and_async_middleware
def HistoryRequestMiddleware(get_response): # -> Callable[..., CoroutineType[Any, Any, Any]] | Callable[..., Any]:
    ...

