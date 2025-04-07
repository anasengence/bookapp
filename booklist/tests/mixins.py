class AuthMixin:
    def authenticate(self, client, user):
        client.force_authenticate(user=user)
