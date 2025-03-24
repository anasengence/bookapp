from django.contrib import admin

from booklist.models import Book, Author, Genre

# Register your models here.
admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Genre)