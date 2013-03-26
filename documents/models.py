from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth.models import User
from docviewer.models import Document as Docviewer_Document
from guardian.shortcuts import get_users_with_perms


class Document(Docviewer_Document):
    """ A document with its minimum requiered fields """
    source = models.CharField(
        _('Source'), blank=True, null=False, max_length=50,
        help_text=_('The source of the document'))
    notes = models.TextField(
        _('Notes'), null=True, blank=True,
        help_text=_('Notes of the book'))
    public = models.BooleanField(
        _('Publicly Available'), blank=False, null=False,
        help_text=_('Is this document available to everybody?'))
    owner = models.ForeignKey(User, blank=False, null=False)

    def get_users_with_perms(self):
        return get_users_with_perms(
            self, attach_perms=False, with_superusers=False,
            with_group_users=False).exclude(id=self.owner.id)

    class Meta:
        permissions = (
            ('access_document', _('Access Document')),
        )
