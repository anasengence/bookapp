from django.urls import path, include
from .v1 import views as v1_views
from .v2 import views as v2_views
from rest_framework.routers import DefaultRouter

# from .views import (
#     BookList,
#     BookDetail,
#     AuthorList,
#     AuthorDetail,
#     GenreList,
#     GenreDetail,
# )

# router = DefaultRouter()
# router.register(r"books", v1_views.BookViewSet, basename="get-books")
# router.register(r"authors", v1_views.AuthorViewSet, basename="get-authors")
# router.register(r"genres", v1_views.GenreViewSet, basename="get-genres")

# urlpatterns = [
#     path("books/", BookList.as_view(), name="get-books"),
#     path("books/<int:pk>/", BookDetail.as_view(), name="get-books-detail"),
#     path("authors/", AuthorList.as_view(), name="get-authors"),
#     path("authors/<int:pk>/", AuthorDetail.as_view(), name="get-authors-detail"),
#     path("genres/", GenreList.as_view(), name="get-genres"),
#     path("genres/<int:pk>/", GenreDetail.as_view(), name="get-genres-detail"),
# ]

# urlpatterns = router.urls  # This is also correct
# urlpatterns = [*router.urls]     # This is also correct

# Create a router for version 1 of your API
v1_router = DefaultRouter()
v1_router.register(
    r"books", v1_views.BookViewSet, basename="books"
)  # Using "books" as basename
v1_router.register(
    r"authors", v1_views.AuthorViewSet, basename="authors"
)  # Using get-authors as basename
v1_router.register(r"genres", v1_views.GenreViewSet, basename="genres")

# Create and register routes for version 2 of the API
v2_router = DefaultRouter()
v2_router.register(r"books", v2_views.BookViewSet, basename="books-v2")
v2_router.register(r"authors", v2_views.AuthorViewSet, basename="authors-v2")
v2_router.register(r"genres", v2_views.GenreViewSet, basename="genres-v2")

urlpatterns = [
    path("api/v1/", include((v1_router.urls, "v1"), namespace="v1")),
    path("api/v2/", include((v2_router.urls, "v2"), namespace="v2")),
    # path("api/", include((v2_router.urls, app_name), namespace="default")),
    # path("api/", include(v1_router.urls)),
    path("api/", include((v2_router.urls, "default"), namespace="default")),
]
