import requests
from django import forms
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.forms.util import flatatt
from django.utils.safestring import mark_safe
from docviewer.forms import DocumentForm as Docviewer_DocumentForm
from docviewer.models import Annotation
from models import Document
from taggit.models import Tag
from widgets import AnchorField
from io import BytesIO


class DocumentAdminForm(Docviewer_DocumentForm):
    class Meta:
        model = Document

    description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'vLargeTextField'}),
        help_text=_('Description of the document'))


SOURCES = (
    ('local', _('Your computer')),
    ('dropbox', _('Dropbox')),
)

class DocumentForm(Docviewer_DocumentForm):
    source = forms.ChoiceField(
        label=_('Choose document from'),
        choices=SOURCES,
        widget=forms.RadioSelect,
        initial='local',
    )
    docfile = forms.FileField(label=_('Document'), required=False)
    external_url = forms.CharField(
        label=_('Document'),
        required=False,
        widget=forms.HiddenInput(),
    )
    class Meta:
        model = Document
        fields = ('source', 'docfile', 'external_url', 'language', 'public', 'title', 'notes')

    notes = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={'class': 'vLargeTextField', 'rows': 3}),
        help_text=None)
    public = forms.BooleanField(
        label=_('Publicly available'), required=False, help_text=None)

    class Media:
        js = (
            'js/source.js',
        )

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

    def clean(self):
        source = self.cleaned_data['source']
        docfile = self.cleaned_data['docfile']
        external_url = self.cleaned_data['external_url']
#        empty_file = not docfile
#        empty_url = not external_url or len(external_url) == 0
#        if empty_file and empty_url:
#            raise forms.ValidationError('Choose a PDF document either from Dropbox or from your local machine.')
#        elif empty_file and not empty_url:
#            self.cleaned_data['docfile'] = upload_file_from_url(external_url)
        if source == 'local' and docfile:
            pass
        elif source == 'dropbox' and external_url:
            self.cleaned_data['docfile'] = upload_file_from_url(external_url)
        else:
            raise forms.ValidationError('Choose a PDF document either from Dropbox or from your local machine.')
        return self.cleaned_data


class CloneForm(forms.Form):
    pages = forms.BooleanField(
        label=_('Pages'),
        required=False,
        initial=True,
    )
    collaborators = forms.BooleanField(
        label=_('Collaborators'),
        required=False,
    )
    tags = forms.BooleanField(
        label=_('Tags'),
        required=False,
    )
    annotations = forms.BooleanField(
        label=_('Annotations'),
        required=False,
    )
    editions = forms.BooleanField(
        label=_('Edition history'),
        required=False,
    )
    zotero = forms.BooleanField(
        label=_('Zotero metadata'),
        required=False,
    )
    all_fields = forms.BooleanField(
        label=_('All'),
        required=False,
    )
    
    def __init__(self, *args, **kwargs):
        super(CloneForm, self).__init__(*args, **kwargs)
        self.fields['pages'].widget.attrs['disabled'] = True
    
    class Media:
        js = (
            'js/clone.js',
        )


def upload_file_from_url(url):
    filefield_name = u'docfile'
    file_type = u'application/pdf'
    
    f = download_file(url)
    local_filename = url.split('/')[-1]
    return create_InMemoryUploadedFile(
        f,
        local_filename,
        filefield_name,
        file_type,
    )


def download_file(url):
    req = requests.get(url, stream=True)
    f = BytesIO()
    for chunk in req.iter_content(chunk_size=1024):
        f.write(chunk)
    return f


def create_InMemoryUploadedFile(f, filename, fieldname, filetype):
    f.seek(0, 2)
    size = f.tell()
    return InMemoryUploadedFile(f, fieldname, filename, filetype, size, None)


class EditDocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('docfile', 'language', 'public', 'title', 'notes')

    docfile = AnchorField(label=_('Document'))
    language = forms.ChoiceField(
          choices=Document.LANGUAGES, required=False, help_text=None)
#    source = forms.CharField(required=False, help_text=None)
    public = forms.BooleanField(
        label=_('Publicly available'), required=False, help_text=None)
    notes = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={'class': 'vLargeTextField', 'rows': 3}),
        help_text=None)

    def __init__(self, *args, **kwargs):
        super(EditDocumentForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['language'].widget.attrs['disabled'] = True


    def clean_language(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.language
        else:
            return self.cleaned_data['language']



class SearchDocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('title', )
    title = forms.CharField(required=False)
    annotations = forms.CharField(required=False)
    tags = forms.CharField(required=False)
