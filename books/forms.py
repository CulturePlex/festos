from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from haystack.forms import SearchForm
from haystack.query import SearchQuerySet
from docviewer.forms import DocumentForm
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
        fields = ('title', 'author', 'file', 'source', 
                  'description', 'notes', 'public')

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
    public = forms.BooleanField(label=_('Publicly available'), required=False,
              help_text=None)

    def __init__(self, *args, **kwargs):
        try:
            self._user = kwargs.pop('user')
        except:
            self._user = User.objects.get(username="festos")
        super(BookForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        inst = super(BookForm, self).save(commit=False)
        inst.owner = self._user
        if commit:
            inst.save()
        return inst

class EditBookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ('title', 'author', 'source', 
                  'description', 'notes', 'public' )

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
    public = forms.BooleanField(label=_('Publicly available'), required=False,
              help_text=None)


class SearchBookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ('title', 'author', 'source', 
                  'description', 'notes')
    title = forms.CharField(required=False)
    author = forms.CharField(required=False)
    description = forms.CharField(required=False)
    notes = forms.CharField(required=False)
    source = forms.CharField(required=False)

