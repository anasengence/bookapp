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
router.register(r"books", BookViewSet, basename="get-books")
router.register(r"authors", AuthorViewSet, basename="get-authors")
router.register(r"genres", GenreViewSet, basename="get-genres")

# urlpatterns = [
#     path("books/", BookList.as_view(), name="get-books"),
#     path("books/<int:pk>/", BookDetail.as_view(), name="get-books-detail"),
#     path("authors/", AuthorList.as_view(), name="get-authors"),
#     path("authors/<int:pk>/", AuthorDetail.as_view(), name="get-authors-detail"),
#     path("genres/", GenreList.as_view(), name="get-genres"),
#     path("genres/<int:pk>/", GenreDetail.as_view(), name="get-genres-detail"),
# ]

urlpatterns = router.urls  # This is also correct
# urlpatterns = [*router.urls]     # This is also correct
