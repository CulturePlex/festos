from django.contrib import admin
from docviewer.admin import DocumentAdmin

from books.forms import BookForm
from books.models import Book


class BookAdmin(DocumentAdmin):

    form = BookForm
    fieldsets = [
             ('Book details', {'fields': ['author']}),
    ]
    fieldsets.insert(1, DocumentAdmin.fieldsets[0])


admin.site.register(Book, BookAdmin)
