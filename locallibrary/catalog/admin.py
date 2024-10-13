from django.contrib import admin
from .models import Book, Author, Genre, BookInstance, Language, Publisher
# Register your models here.


#username = admin
#password = admin123


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name')

admin.site.register(Author, AuthorAdmin)

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')

admin.site.register(Book, BookAdmin)

class BookInstanceAdmin(admin.ModelAdmin):
    list_filter = ('status', 'due_back')

    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back')
        }),
    )

admin.site.register(BookInstance, BookInstanceAdmin)

admin.site.register(Genre)
admin.site.register(Publisher)
admin.site.register(Language)   