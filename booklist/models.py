from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField()
    date_of_birth = models.DateField()

    def __str__(self):
        return self.name


# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(
        Author, on_delete=models.CASCADE, related_name="author_books"
    )
    date_published = models.DateField()
    genre = models.ManyToManyField("Genre")

    def __str__(self):
        return self.title


class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
