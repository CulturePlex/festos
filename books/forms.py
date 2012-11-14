from django import forms
from docviewer.forms import DocumentForm
from django.utils.translation import ugettext_lazy as _
from books.models import Book

class BookForm(DocumentForm):
    class Meta:
        model = Book

    title = forms.CharField(
            widget=forms.TextInput(attrs={'class':'vTextField'}),
            help_text=_("The title of the book"))
    file = forms.FileField(
           label=_('Upload Book'), 
           help_text=_('Select your scan book'))
    source_url = forms.URLField(
                 required=False,
                 widget=forms.TextInput(attrs={'class':'vTextField'}),
                 label = _('Source URL of the book'), 
                 help_text=_('Where does this book come from?'))
    description = forms.CharField(
            required=False,
            widget=forms.Textarea(attrs={'class':'vLargeTextField'}),
            help_text=_('Description of the book'))

