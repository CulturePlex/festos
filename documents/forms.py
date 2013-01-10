from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from haystack.forms import SearchForm
from haystack.query import SearchQuerySet
from docviewer.forms import DocumentForm as Docviewer_DocumentForm
from models import Document, Reference


class DocumentAdminForm(Docviewer_DocumentForm):
    class Meta:
        model = Document

    title = forms.CharField(
            widget=forms.TextInput(attrs={'class':'vTextField'}),
            help_text=_("The title of the document"))
    file = forms.FileField(
           label=_('Upload Document'), 
           help_text=_('Select your pdf scanned document'))
    description = forms.CharField(
            required=False,
            widget=forms.Textarea(attrs={'class':'vLargeTextField'}),
            help_text=_('Description of the document'))
            



class DocumentForm(Docviewer_DocumentForm):
    class Meta:
        model = Document
        fields = ('title', 'author', 'file', 'source', 
                  'description', 'notes', 'public','reference')

    title = forms.CharField(help_text=None)
    author = forms.CharField(help_text=None)
    file = forms.FileField(
           label=_('Upload Document'), 
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
        super(DocumentForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        inst = super(DocumentForm, self).save(commit=False)
        inst.owner = self._user
        if commit:
            inst.save()
        return inst

class EditDocumentForm(forms.ModelForm):
    class Meta:
        model = Document
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

class SearchReferenceForm(forms.ModelForm):
    class Meta:
        model = Reference
        fields = ('editorial',) #the comma is necessary :S
    editorial = forms.CharField(required=False)

class SearchDocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('title', 'author', 'source', 
                  'description', 'notes')
    title = forms.CharField(required=False)
    author = forms.CharField(required=False)
    description = forms.CharField(required=False)
    notes = forms.CharField(required=False)
    source = forms.CharField(required=False)
 
    


