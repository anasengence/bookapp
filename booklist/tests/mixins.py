from rest_framework_simplejwt.tokens import RefreshToken


class AuthMixin:
    def authenticate(self, client, user):
        # Generate JWT token for the user
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        # Set the token in the client's Authorization header
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
        return access_token