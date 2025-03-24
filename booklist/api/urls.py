from django.urls import path
from .views import BookList, BookDetail, AuthorList, AuthorDetail, GenreList, GenreDetail

urlpatterns = [
    path("books/", BookList.as_view(), name="get_books"),
    path("books/<int:pk>/", BookDetail.as_view(), name="get_books_detail"),
    path("authors/", AuthorList.as_view(), name="get_authors"),
    path("authors/<int:pk>/", AuthorDetail.as_view(), name="get_authors_detail"),
    path("genres/", GenreList.as_view(), name="get_genres"),
    path("genres/<int:pk>/", GenreDetail.as_view(), name="get_genres_detail"),
]
