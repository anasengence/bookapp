from django.urls import resolve
from django.test import SimpleTestCase
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from ..models import Author, Book, Genre
from datetime import date
from django.contrib.auth.models import User
from .mixins import AuthMixin
from .factory import CustomAPIRequestFactory


# class BookAPITestCase(AuthMixin, APITestCase):
# def setUp(self):
#     self.genre = Genre.objects.create(name="Fiction")
#     self.author = Author.objects.create(
#         name="John Doe", bio="Writer", date_of_birth="1980-01-01"
#     )
#     self.book = Book.objects.create(
#         title="Test Book", author=self.author, date_published=date(2023, 1, 1)
#     )
#     self.book.genre.add(self.genre)
#     self.user = User.objects.create_user(username="testuser", password="pass123")

# def test_get_books(self):
#     url = reverse("v1:books-list")  # DRF appends -list to the basename
#     response = self.client.get(url)
#     self.assertEqual(response.status_code, 200)

# def test_filter_books_by_date(self):
#     url = reverse("v1:books-list")
#     response = self.client.get(url, {"date_published": "2023-01-01"})
#     self.assertEqual(len(response.data["results"]), 1)

# def test_pagination_limit_offset(self):
#     url = reverse("v1:books-list") + "?limit=1&offset=0"
#     response = self.client.get(url)
#     self.assertIn("results", response.data)

# def test_ordering_books(self):
#     url = reverse("v1:books-list") + "?ordering=-date_published"
#     response = self.client.get(url)
#     self.assertEqual(response.status_code, 200)

# def test_auth_required(self):
#     url = reverse("v1:authors-list")
#     response = self.client.get(url)
#     self.assertEqual(response.status_code, 401)

# def test_authenticated_access(self):
#     # Authenticate using JWT token
#     self.authenticate(self.client, self.user)
#     url = reverse("v1:authors-list")
#     response = self.client.get(url)
#     self.assertEqual(response.status_code, 200)


class BookAPITestCase(AuthMixin, APITestCase):
    def setUp(self):
        # Initialize factories
        self.factory = CustomAPIRequestFactory()  # Unauthenticated factory
        self.genre = Genre.objects.create(name="Fiction")
        self.author = Author.objects.create(
            name="John Doe", bio="Writer", date_of_birth="1980-01-01"
        )
        self.book = Book.objects.create(
            title="Test Book", author=self.author, date_published=date(2023, 1, 1)
        )
        self.book.genre.add(self.genre)
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )

        # Authenticate and get token for authenticated factory
        self.access_token = self.authenticate(self.client, self.user)
        self.auth_factory = self.factory.with_auth(self.user)  # Authenticated factory

    def _call_view(self, request, url):
        """
        Helper to resolve and call the view with the request.
        Works with router-generated views for ModelViewSet.
        """
        # Ensure url is a clean path for resolution
        clean_url = url.split("?")[0]
        print(f"Resolving URL: {clean_url}")  # Debug output
        view_info = resolve(clean_url)
        view = view_info.func
        request.method = request.META["REQUEST_METHOD"]
        response = view(request)
        return response

    def test_get_books(self):
        url = reverse("v1:books-list")
        request = self.factory.create_request("GET", url)
        response = self._call_view(request, url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filter_books_by_date(self):
        url = reverse("v1:books-list")
        request = self.factory.create_request(
            "GET", url, data={"date_published": "2023-01-01"}
        )
        response = self._call_view(request, url)
        response.render()
        self.assertEqual(len(response.data["results"]), 1)

    def test_pagination_limit_offset(self):
        url = reverse("v1:books-list")
        request = self.factory.create_request("GET", url, data={"limit": "1", "offset": "0"})
        response = self._call_view(request, url)
        response.render()
        self.assertIn("results", response.data)

    def test_ordering_books(self):
        url = reverse("v1:books-list") + "?ordering=-date_published"
        request = self.factory.create_request("GET", url)
        response = self._call_view(request, url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_auth_required(self):
        url = reverse("v1:authors-list")
        request = self.factory.create_request("GET", url)  # Unauthenticated
        response = self._call_view(request, url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_access(self):
        url = reverse("v1:authors-list")
        request = self.auth_factory.create_request("GET", url)
        response = self._call_view(request, url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
