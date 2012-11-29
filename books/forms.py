from django import forms
from docviewer.forms import DocumentForm
from django.utils.translation import ugettext_lazy as _
from books.models import Book

class BookAdminForm(DocumentForm):
    class Meta:
        model = Book

    title = forms.CharField(
            widget=forms.TextInput(attrs={'class':'vTextField'}),
            help_text=_("The title of the book"))
    file = forms.FileField(
           label=_('Upload Book'), 
           help_text=_('Select your pdf scanned book'))
    description = forms.CharField(
            required=False,
            widget=forms.Textarea(attrs={'class':'vLargeTextField'}),
            help_text=_('Description of the book'))


class BookForm(DocumentForm):
    class Meta:
        model = Book
        fields = ('title', 'author', 'file', 'description', 'notes', 'source')

    title = forms.CharField(
            help_text=_("The title of the book"))
    file = forms.FileField(
           label=_('Upload Book'), 
           help_text=_('Select your pdf scanned book'))
    description = forms.CharField(
            required=False,
            help_text=_('Description of the book'))

