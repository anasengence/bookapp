from datetime import date
from django.urls import reverse
from django.test import TestCase
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from .models import Author, Book, Genre
from .api.serializers import BookSerializer
from django.contrib.auth.models import User

class PermissionTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser('admin', 'admin@test.com', 'password')
        self.staff = User.objects.create_user('staff', 'staff@test.com', 'password', is_staff=True)
        self.user = User.objects.create_user('user', 'user@test.com', 'password')
        self.book = Book.objects.create(title="Test Book")

    def test_owner_permission(self):
        client = APIClient()
        client.force_authenticate(user=self.user)
        response = client.patch(f'/books/{self.book.id}/', {'title': 'New Title'})
        self.assertEqual(response.status_code, 200)

    def test_field_permissions(self):
        client = APIClient()
        client.force_authenticate(user=self.staff)
        response = client.get(f'/books/{self.book.id}/')
        self.assertIn('price', response.data)  # Staff can see price
        
        client.force_authenticate(user=self.user)
        response = client.get(f'/books/{self.book.id}/')
        self.assertNotIn('price', response.data)  # Regular user can't see price


class BookSerializerTestCase(TestCase):
    def setUp(self):
        self.author = Author.objects.create(
            name="Jaan", date_of_birth=date(1980, 1, 1), bio="here we go"
        )
        self.genre = Genre.objects.create(name="happy")

        self.valid_data = {
            "title": "Suiii",
            "date_published": "2020-05-20",
            "author": self.author.id,
            "genre": [self.genre.pk],
        }

        self.invalid_data_1 = {
            "title": self.author.name,
            "date_published": "2020-05-20",
            "author": self.author.id,
            "genre": [self.genre.pk],
        }

        self.invalid_data_2 = {
            "title": "No Suiii",
            "date_published": "2025-05-20",
            "author": self.author.id,
            "genre": [self.genre.pk],
        }

    def test_serialization(self):
        book = Book.objects.create(
            title="Mein hoon book",
            date_published=date(2020, 5, 20),
            author=self.author,
        )
        book.genre.add(self.genre)

        serializer = BookSerializer(book, context={"request": None})
        data = serializer.data

        self.assertEqual(data["title"], "Mein hoon book")
        # print(data)
        self.assertEqual(data["author_name"], self.author.name)
        self.assertIn("genre_details", data)
        self.assertIn(self.genre.name, data["genre_details"][0]["name"])

    def test_deserialization_and_validation(self):
        serializer = BookSerializer(data=self.valid_data, context={"request": None})
        self.assertTrue(serializer.is_valid(), serializer.errors)
        book = serializer.save()
        self.assertEqual(book.title, self.valid_data["title"])
        self.assertEqual(book.author, self.author)
        self.assertIn(self.genre, book.genre.all())

        serializer = BookSerializer(data=self.invalid_data_1, context={"request": None})
        self.assertFalse(serializer.is_valid())
        self.assertIn("non_field_errors", serializer.errors)

        serializer = BookSerializer(data=self.invalid_data_2, context={"request": None})
        self.assertFalse(serializer.is_valid())
        self.assertIn("date_published", serializer.errors)


class AuthorViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.author = Author.objects.create(name="CR-7", date_of_birth=date(1980, 1, 1))
        self.book = Book.objects.create(
            title="Goat vs King", date_published=date(2020, 5, 20), author=self.author
        )
        genre = Genre.objects.create(name="Sports")
        self.book.genre.add(genre)

    def test_get_authors(self):
        url = reverse("get-authors")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(
            any(author["name"] == self.author.name for author in response.data)
        )

    def test_create_author(self):
        url = reverse("get-authors")
        data = {
            "name": "Anas tahir",
            "bio": "here we go",
            "date_of_birth": "2000-11-23",
        }
        response = self.client.post(url, data, format="json")
        # print(response.json())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "Anas tahir")
