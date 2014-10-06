import os
import shutil
from copy import deepcopy
from django.db.models.signals import post_save
from docviewer.models import document_save
from django_zotero.models import Tag
from guardian.shortcuts import assign_perm
from documents.utils import rename_files_recursively

from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth.models import User
from docviewer.models import Document as Docviewer_Document, Page, Annotation, Edition
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
    
    def clone(self):
        """ It clones pages, annotations, editions and zotero tags.
            It copies collaborators and taggit tags."""
        # Clone document
        new = deepcopy(self)
        new.id = None
        new.pk = None
        new.slug = None
        new.save()
        # Clone pages
        pages = self.pages_set.all()
        for page in pages:
            new.pages_set.create(
                page=page.page,
                modified=page.modified,
            )
        # Clone annotations
        anns = self.annotations_set.all()
        for ann in anns:
            new.annotations_set.create(
                title=ann.title,
                location=ann.title,
                page=ann.page,
                content=ann.content,
                author=ann.author,
            )
        # Clone editions
        edits = self.editions_set.all()
        for edit in edits:
            new.editions_set.create(
                date=edit.date,
                date_string=edit.date_string,
                modified_pages=edit.modified_pages,
                comment=edit.comment,
                author=edit.author,
            )
        # Clone zotero tags
        z_tags = Tag.get_tags(self)
        for tag in z_tags:
            new_t = deepcopy(tag)
            new_t.set_object(new)
            new_t.id = None
            new_t.pk = None
            new_t.save()
        # Copy collaborators
        collabs = self.get_users_with_perms()
        for collab in collabs:
            assign_perm('documents.access_document', collab, new)
        # Copy taggit tags
        t_tags = self.taggit_tags.all()
        for tag in t_tags:
            new.taggit_tags.add(tag.name)
        # Duplicate directories and files
        old_dir = self.get_root_path()
        new_dir = new.get_root_path()
        shutil.copytree(old_dir, new_dir)
        path = os.path.join('media', new_dir)
        old_slug = self.slug
        new_slug = new.slug
        rename_files_recursively(path, old_slug, new_slug)

    class Meta:
        permissions = (
            ('access_document', _('Access Document')),
        )
