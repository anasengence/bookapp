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
    permission_field = serializers.SerializerMethodField()
    summary = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        # Pop the request from the context
        super().__init__(*args, **kwargs)
        request = self.context.get("request")
        if not (request and request.user and request.user.is_staff):
            # If user is not admin, remove the permission_field field
            self.fields.pop("permission_field", None)
            
        if request:
            include_summary = request.query_params.get("summary").lower() == "true"
            if not include_summary:
                self.fields.pop("summary", None)
    
    def get_permission_field(self, obj):
        # Provide extra info only if required
        return f"Sensitive details for {obj.title}"
    
    def get_summary(self, obj):
        return f"{obj.title} was published on {obj.date_published}"

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


class BookListSerializer(BookSerializer):
    author_name = serializers.StringRelatedField(source="author", read_only=True)

    class Meta(BookSerializer.Meta):
        model = Book
        fields = ["id", "title", "author_name", "date_published"]


# Serializer for detail view (more fields and nested representation)
class BookDetailSerializer(BookSerializer):
    author = AuthorSerializer(read_only=True)
    genre_details = GenreSerializer(source="genre", many=True, read_only=True)

    class Meta(BookSerializer.Meta):
        model = Book
        # You might want to include all fields for the detail view.
        fields = "__all__"
