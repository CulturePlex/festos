import os
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.forms.util import flatatt
from django.utils.safestring import mark_safe
from docviewer.forms import DocumentForm as Docviewer_DocumentForm
from models import Document


class DocumentAdminForm(Docviewer_DocumentForm):
    class Meta:
        model = Document

    description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'vLargeTextField'}),
        help_text=_('Description of the document'))


class DocumentForm(Docviewer_DocumentForm):
    class Meta:
        model = Document
        fields = ('docfile', 'language', 'public', 'source', 'notes')

    notes = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={'class': 'vLargeTextField', 'rows': 3}),
        help_text=None)
    source = forms.CharField(required=False, help_text=None)
    public = forms.BooleanField(
        label=_('Publicly available'), required=False, help_text=None)

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



class AnchorOnlyWidget(forms.Widget):
    def render(self, name, value, attrs):
        final_attrs = self.build_attrs(attrs, name=name)
        if hasattr(self, 'initial'):
            value = self.initial
        return mark_safe(
            "<p style='padding-top:4px'><a href='%s' %s>%s</a></p>" %
                (os.path.join(settings.MEDIA_ROOT,value.name),
                flatatt(final_attrs),
                value.name.split('/')[-1]))

    def _has_changed(self, initial, data):
        return False

class AnchorOnlyField(forms.FileField):
    widget = AnchorOnlyWidget
    def __init__(self, widget=None, label=None, initial=None, help_text=None):
        forms.Field.__init__(self, label=label, initial=initial,
            help_text=help_text, widget=widget)

    def clean(self, value, initial):
        self.widget.initial = initial
        return initial



class EditDocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('docfile','language', 'source', 'public', 'notes', )

    docfile = AnchorOnlyField()
    language = forms.CharField(required=False, help_text=None)
    source = forms.CharField(required=False, help_text=None)
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
            self.fields['language'].widget.attrs['readonly'] = True
#            self.fields['docfile'].widget.attrs['readonly'] = True


    def clean_language(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.language
        else:
            return self.cleaned_data['language']


#    def clean_docfile(self):
#        instance = getattr(self, 'instance', None)
#        if instance and instance.pk:
#            return instance.docfile
#        else:
#            return self.cleaned_data['docfile']





class SearchDocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('title', 'source', 'description', 'notes')
    title = forms.CharField(required=False)
    description = forms.CharField(required=False)
    notes = forms.CharField(required=False)
    source = forms.CharField(required=False)
