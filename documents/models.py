import os
import shutil
from copy import deepcopy
from docviewer.models import document_save

from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth.models import User
from docviewer.models import (
    Document as Docviewer_Document, Page, Annotation, Edition)
from guardian.shortcuts import get_users_with_perms

from documents.tasks import task_clone_document


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
    
    def clone(self, user, options):
        """ It clones pages, annotations, editions and zotero tags.
            It copies collaborators and taggit tags."""
        # Clone document
        new = deepcopy(self)
        new.id = None
        new.pk = None
        new.slug = None
        new.owner = User.objects.get(username=user)
        new.status = self.STATUS.copying
        new.task_error = ''
        new.add_info('cloned', self.get_absolute_url())
        new.save()
        # Clone
        args = [self.id, new.id, options]
        task = task_clone_document.apply_async(args=args, countdown=5)
        new.task_id = task.task_id
        new.save()

    class Meta:
        permissions = (
            ('access_document', _('Access Document')),
        )
