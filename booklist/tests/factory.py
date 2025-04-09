from rest_framework.test import APIRequestFactory
from rest_framework_simplejwt.tokens import RefreshToken


class CustomAPIRequestFactory(APIRequestFactory):
    def __init__(self, default_headers=None):
        super().__init__()
        self.default_headers = default_headers or {}

    def create_request(
        self, method, path, data=None, authenticated=False, user=None, **extra
    ):
        """
        Create a request with optional authentication and custom headers.
        """
        method_func = getattr(self, method.lower())
        clean_path = path.split("?")[0]
        request = method_func(clean_path, data=data, **extra)
        request.META.update(self.default_headers)
        if authenticated and user:
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            request.META["HTTP_AUTHORIZATION"] = f"Bearer {access_token}"
        return request

    def with_auth(self, user):
        """Helper to create an authenticated factory instance"""
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        headers = {"HTTP_AUTHORIZATION": f"Bearer {access_token}"}
        return CustomAPIRequestFactory(default_headers=headers)
