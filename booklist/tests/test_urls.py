from django.urls import resolve
from django.test import SimpleTestCase


class URLPatternsTestCase(SimpleTestCase):
    def test_book_list_url_resolves(self):
        resolver = resolve("/api/v1/books/")
        self.assertEqual(resolver.url_name, "books-list")

    def test_author_list_url_resolves(self):
        resolver = resolve("/api/v1/authors/")
        self.assertEqual(resolver.url_name, "authors-list")
