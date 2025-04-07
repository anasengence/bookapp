from rest_framework.test import APIRequestFactory

class CustomAPIRequestFactory(APIRequestFactory):
    def get_with_user(self, path, user):
        request = self.get(path)
        request.user = user
        return request
