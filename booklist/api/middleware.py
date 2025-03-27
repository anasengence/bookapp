from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.utils.deprecation import MiddlewareMixin

class JWTAuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        try:
            user_auth = JWTAuthentication().authenticate(request)
            if user_auth is not None:
                request.user, request.auth = user_auth
        except (InvalidToken, TokenError):
            raise InvalidToken("Invalid token by Middleware")