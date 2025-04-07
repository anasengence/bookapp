from django.urls import resolve
from django.test import SimpleTestCase
from rest_framework.test import APITestCase
from django.urls import reverse
from ..models import Author, Book, Genre
from datetime import date
from django.contrib.auth.models import User


class BookAPITestCase(APITestCase):
    def setUp(self):
        self.genre = Genre.objects.create(name="Fiction")
        self.author = Author.objects.create(
            name="John Doe", bio="Writer", date_of_birth="1980-01-01"
        )
        self.book = Book.objects.create(
            title="Test Book", author=self.author, date_published=date(2023, 1, 1)
        )
        self.book.genre.add(self.genre)

    def test_get_books(self):
        url = reverse("v1:books-list")  # DRF appends -list to the basename
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_filter_books_by_date(self):
        url = reverse("v1:books-list")
        response = self.client.get(url, {"date_published": "2023-01-01"})
        self.assertEqual(len(response.data["results"]), 1)

    def test_pagination_limit_offset(self):
        url = reverse("v1:books-list") + "?limit=1&offset=0"
        response = self.client.get(url)
        self.assertIn("results", response.data)

    def test_ordering_books(self):
        url = reverse("v1:books-list") + "?ordering=-date_published"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_auth_required(self):
        url = reverse("v1:authors-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)
