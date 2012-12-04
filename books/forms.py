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
        fields = ('title', 'author', 'file', 'source', 'description', 'notes' )

    title = forms.CharField(help_text=None)
    author = forms.CharField(help_text=None)
    file = forms.FileField(
           label=_('Upload Book'), 
           help_text=None)
    description = forms.CharField(
            required=False,
            widget=forms.Textarea(attrs={'class':'vLargeTextField','rows':3}),
            help_text=None)
    notes = forms.CharField(
            required=False,
            widget=forms.Textarea(attrs={'class':'vLargeTextField','rows':3}),
            help_text=None)
    source = forms.CharField(required=False,help_text=None)
    
class EditBookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ('title', 'author', 'source', 'description', 'notes' )

    title = forms.CharField(help_text=None)
    author = forms.CharField(help_text=None)
    description = forms.CharField(
            required=False,
            widget=forms.Textarea(attrs={'class':'vLargeTextField','rows':3}),
            help_text=None)
    notes = forms.CharField(
            required=False,
            widget=forms.Textarea(attrs={'class':'vLargeTextField','rows':3}),
            help_text=None)
    source = forms.CharField(required=False,help_text=None)


