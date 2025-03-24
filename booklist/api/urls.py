from django.urls import path
from .views import (
    BookViewSet,
    AuthorViewSet,
    GenreViewSet,
)
from rest_framework.routers import DefaultRouter

# from .views import (
#     BookList,
#     BookDetail,
#     AuthorList,
#     AuthorDetail,
#     GenreList,
#     GenreDetail,
# )

router = DefaultRouter()
router.register(r"books", BookViewSet, basename="books")
router.register(r"authors", AuthorViewSet, basename="authors")
router.register(r"genres", GenreViewSet, basename="genres")

# urlpatterns = [
#     path("books/", BookList.as_view(), name="get_books"),
#     path("books/<int:pk>/", BookDetail.as_view(), name="get_books_detail"),
#     path("authors/", AuthorList.as_view(), name="get_authors"),
#     path("authors/<int:pk>/", AuthorDetail.as_view(), name="get_authors_detail"),
#     path("genres/", GenreList.as_view(), name="get_genres"),
#     path("genres/<int:pk>/", GenreDetail.as_view(), name="get_genres_detail"),
# ]

urlpatterns = router.urls      # This is also correct
# urlpatterns = [*router.urls]     # This is also correct