from django.db import models
from django.db.models import UniqueConstraint
from django.db.models.functions import Lower

from django.urls import reverse
import uuid

# Create your models here.

class Genre(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('genre-detail', args=[str(self.id)])
    
    class Meta:
        constraints = [
            #By using Lower('name'), it ensure that Django treats "Science", "science", and "SCIENCE" as the same value
            UniqueConstraint(
                Lower('name'),
                name='genre_name_case_insensitive_unique'
            ),
        ]

class Publisher(models.Model):
    name = models.CharField(max_length=200, unique=True)
    website = models.URLField(max_length=200)
    city = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Language(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name
    
class Book(models.Model):
     title = models.CharField(max_length=200)
     author = models.ManyToManyField('Author')
     summary = models.TextField(max_length=200)
     isbn = models.CharField('ISBN', max_length=13, unique=True)
     genre = models.ManyToManyField(Genre)
     publisher = models.ForeignKey(Publisher, on_delete=models.SET_NULL, null=True)
     languages = models.ManyToManyField(Language)

     def __str__(self):
         return self.title
     
     def get_absolute_url(self):
         return reverse('book-detail', args=[str(self.id)])
     
class BookInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    book = models.ForeignKey('Book', on_delete=models.RESTRICT, null=True)
    imprint = models.CharField(max_length=200) # publisher/editer detail
    due_back = models.DateField(null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='m', help_text='Book availability')

    class Meta:
        ordering = ['due_back']

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.id} ({self.book.title})'
    
class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']
        
    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])
        
    def __str__(self):
        return f'{self.last_name}, {self.first_name}'