from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth.models import User
from docviewer.models import Document as Docviewer_Document



# Create your models here.
class Document(Docviewer_Document):
    author = models.CharField(_('Author'), blank=False, null=False, 
        max_length=100, help_text='The name of the author of this book')
    notes = models.TextField(_('Notes'), null=True, blank=True, 
        help_text='Notes of the book')
    source = models.CharField(_('Source'), blank=True, null=False, 
        max_length=50, help_text='The source of the document')
    public = models.BooleanField(_('Publicly Available'), blank = False,
            null=False, help_text='Is this document available to everybody?')
    owner = models.ForeignKey(User, blank = False, null = False)

