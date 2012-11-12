from django import forms
from docviewer.forms import DocumentForm
from django.utils.translation import ugettext_lazy as _
from books.models import Book

class BookForm(DocumentForm):
    class Meta:
        model = Book
