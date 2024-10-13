from django.db import models
from django.db.models import UniqueConstraint
from django.db.models.functions import Lower

from django.urls import reverse
import uuid

# Create your models here.

class Genre(models.Model):
    name = models.CharField(max_length=200, unique=True, help_text="Enter a book genre (e.g. Science Fiction)")

    def __str__(self):
        return self.name

class Publisher(models.Model):
    name = models.CharField(max_length=200, help_text="Enter the publisher name")

    def __str__(self):
        return self.name

class Language(models.Model):
    name = models.CharField(max_length=100, help_text="Enter the book's language")
    
    def __str__(self):
        return self.name
    
class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.last_name}, {self.first_name}'
    
    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])
    
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)
    summary = models.TextField(max_length=1000, help_text="Enter a brief description of the book")
    isbn = models.CharField('ISBN', max_length=13, unique=True, help_text='13 Character ISBN number')
    genre = models.ManyToManyField(Genre, help_text="Select a genre for this book")
    language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True)
    publisher = models.ForeignKey(Publisher, on_delete=models.SET_NULL, null=True)
     
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])

    def display_genre(self):
        return ', '.join(genre.name for genre in self.genre.all()[:3])

    display_genre.short_description = 'Genre'
     
class BookInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID for this particular book across the library")
    book = models.ForeignKey(Book, on_delete=models.RESTRICT, null=True)
    imprint = models.CharField(max_length=200) # publisher/editer detail
    due_back = models.DateField(null=True, blank=True)

    STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(max_length=1, choices=STATUS, blank=True, default='m', help_text='Book availability')
    
    class Meta:
        ordering = ['due_back']

    def __str__(self):
        return f'{self.id} ({self.book.title})'
    
