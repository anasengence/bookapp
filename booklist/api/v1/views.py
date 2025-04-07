from rest_framework.decorators import api_view, action
from datetime import date
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics

from booklist.api.v1.filter import BookFilter, CustomFilterBackend
from ...models import Book, Author, Genre
from rest_framework import viewsets
from .serializers import (
    BookSerializer,
    BookListSerializer,
    BookDetailSerializer,
    AuthorSerializer,
    CustomTokenObtainPairSerializer,
    GenreSerializer,
)
from .permissions import IsOwner, IsAdminUser, IsStaffUser, IsRegularUser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .pagination import (
    CustomCursorPagination,
    CustomLimitOffsetPagination,
    CustomPageNumberPagination,
)
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class ValidateToken(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(
            {
                "valid": True,
                "user": request.user.username,
                "expires_in": request.auth.payload["exp"],
            }
        )


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


# @api_view(["GET"])
# def getBooks(request):
#     try:
#         books = Book.objects.all()
#         serializer = BookSerializer(books, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     except Exception as e:
#         return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# class AuthorList(generics.ListCreateAPIView):
#     queryset = Author.objects.all()
#     serializer_class = AuthorSerializer


# class AuthorDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Author.objects.all()
#     serializer_class = AuthorSerializer


# class BookList(generics.ListCreateAPIView):
#     queryset = Book.objects.all()
#     serializer_class = BookSerializer


# class BookDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Book.objects.all()
#     serializer_class = BookSerializer


# class GenreList(generics.ListCreateAPIView):
#     queryset = Genre.objects.all()
#     serializer_class = GenreSerializer


# class GenreDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Genre.objects.all()
#     serializer_class = GenreSerializer


#  - Refactor your views to use ViewSets (ModelViewSet)
#    - Implement custom actions with @action decorator
#    - Create a detail action that returns book statistics
#    - Create a list action that returns featured books
#    - Configure DefaultRouter and register your ViewSets


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["name"]
    ordering_fields = ["date_of_birth"]
    ordering = ["date_of_birth"]
    pagination_class = CustomLimitOffsetPagination
    permission_classes = [IsAuthenticated, IsAdminUser]


class BookViewSet(viewsets.ModelViewSet):
    # queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, CustomFilterBackend]
    filterset_fields = ["date_published"]
    filterset_class = BookFilter
    # permission_classes = [IsAuthenticated, IsOwner]
    field_permissions = {
        "title": IsRegularUser,
        "author": IsAdminUser,
        "genre": IsStaffUser,
    }

    def get_queryset(self):
        queryset = Book.objects.all().select_related("author").prefetch_related("genre")
        return queryset

    def get_pagination_class(self):
        paginaton_type = self.request.query_params.get("type")
        if paginaton_type == "cursor":
            return CustomCursorPagination
        elif paginaton_type == "page":
            return CustomPageNumberPagination
        else:
            return CustomLimitOffsetPagination

    pagination_class = property(get_pagination_class)

    def get_serializer_class(self):
        if self.action == "list":
            return BookListSerializer
        elif self.action == "retrieve":
            return BookDetailSerializer
        return BookSerializer

    @action(detail=True, methods=["GET"])
    def stats(self, request, pk=None):
        book = self.get_object()
        return Response(
            {
                "title": book.title,
                "days_since_published": (date.today() - book.date_published).days,
            }
        )

    @action(detail=False, methods=["GET"])
    def featured(self, request):
        featured_books = self.queryset.filter(is_featured=True)
        serializer = self.get_serializer(featured_books, many=True)
        return Response(serializer.data)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = CustomPageNumberPagination
    permission_classes = [IsAuthenticated, IsRegularUser]