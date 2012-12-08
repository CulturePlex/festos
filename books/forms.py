from django import forms
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
        self._user = kwargs.pop('user')
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


class BookSearchForm(SearchForm):
    def search(self, request):
        if not self.is_valid():
            return self.no_query_found()

        if not self.cleaned_data.get('q'):
            return self.no_query_found()

        sqs = SearchQuerySet()
        if request.user.is_authenticated():
            sqs =sqs.filter_or(owner_id=request.user.id).filter_or(public=True)
        else:
            sqs = sqs.filter(public=True)

        sqs = sqs.auto_query(self.cleaned_data['q'])

        if self.load_all:
            sqs = sqs.load_all()

        return sqs
        

