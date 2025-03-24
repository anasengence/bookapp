from rest_framework.decorators import api_view, action
from datetime import date
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics

from booklist.api.filter import BookFilter, CustomFilterBackend
from ..models import Book, Author, Genre
from rest_framework import viewsets
from .serializers import BookSerializer, AuthorSerializer, GenreSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter


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


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, CustomFilterBackend]
    filterset_fields = ["date_published"]
    filterset_class = BookFilter

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
