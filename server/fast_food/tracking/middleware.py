import jwt
from django.conf import settings
from channels.db import database_sync_to_async

class JWTAuthMiddleware:
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):

        headers = dict(scope.get("headers", []))
        token = None

        # Lấy token từ header
        if b"authorization" in headers:
            auth_header = headers[b"authorization"].decode()
            if auth_header.startswith("Bearer "):
                token = auth_header.split(" ")[1]

        # Load user từ token
        scope["user"] = await self.get_user_from_token(token)

        return await self.inner(scope, receive, send)

    @database_sync_to_async
    def get_user_from_token(self, token):
        from django.contrib.auth import get_user_model
        from django.contrib.auth.models import AnonymousUser

        if token is None:
            return AnonymousUser()

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = payload.get("user_id")

            User = get_user_model()
            return User.objects.get(pk=user_id)

        except Exception:
            return AnonymousUser()
