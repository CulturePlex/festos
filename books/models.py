from django.db import models
from django.utils.translation import gettext as _

from docviewer.models import Document


# Create your models here.
class Book(Document):
    author = models.CharField(_('Author'), blank=False, null=False, 
        max_length=50, help_text='The name of the author of this book')
    notes = models.TextField(_('Notes'), null=True, blank=True, 
        help_text='Notes of the book')
