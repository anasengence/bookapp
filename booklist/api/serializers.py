from datetime import date
from rest_framework import serializers
from ..models import Book, Author, Genre


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = "__all__"


class AuthorSerializer(serializers.ModelSerializer):
    author_books = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name="get-books-detail"
    )

    # author_books = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Author
        fields = "__all__"
        # fields = ["id", "name", "bio", "date_of_birth", "author_books"]
        # depth = 1


class BookSerializer(serializers.ModelSerializer):
    # author_name = serializers.CharField(source="author.name", read_only=True)
    author = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all(), write_only=True
    )
    author_name = serializers.StringRelatedField(source="author", read_only=True)
    # days_ago_published = serializers.SerializerMethodField()
    genre_details = GenreSerializer(source="genre", many=True, read_only=True)
    genre = serializers.PrimaryKeyRelatedField(
        queryset=Genre.objects.all(), many=True, write_only=True
    )

    class Meta:
        model = Book
        exclude = ["is_featured"]

    # def get_days_ago_published(self, obj):
    #     days = date.today() - obj.date_published
    #     return days.days

    def validate(self, obj):
        if obj["title"] == obj["author"].name:
            raise serializers.ValidationError(
                "Title and author name cannot be the same"
            )
        return obj

    def validate_date_published(self, value):
        if value.year > 2024:
            raise serializers.ValidationError("Date published cannot be in the future")
        return value
