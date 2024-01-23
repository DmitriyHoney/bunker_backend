from starlette.middleware.base import BaseHTTPMiddleware


class CustomHeaderMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        print("dddd")
        response = await call_next(request)
        print("ddffdd")
        response.headers['Custom'] = 'Example'
        return response