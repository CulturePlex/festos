from django.contrib import admin
from docviewer.admin import DocumentAdmin

from books.forms import BookAdminForm
from books.models import Book

class BookAdmin(DocumentAdmin):

    form = BookAdminForm
    fieldsets = [
             ('Book details', {'fields': ['file','title','author','source',
                                          'description','notes',]}),
    ]
    fieldsets.insert(1, DocumentAdmin.fieldsets[1])

admin.site.register(Book, BookAdmin)
