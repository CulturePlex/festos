import os
import shutil
from copy import deepcopy
from django.db.models.signals import post_save
from docviewer.models import document_save
from django_zotero.models import Tag
from guardian.shortcuts import assign_perm
from documents.utils import dup_dirs_and_files

from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from docviewer.models import (
    Document as Docviewer_Document, Page, Annotation, Edition)
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
    
    def clone(self, user, options):
        """ It clones pages, annotations, editions and zotero tags.
            It copies collaborators and taggit tags."""
        # Clone document
        new = deepcopy(self)
        new.id = None
        new.pk = None
        new.slug = None
        new.owner = User.objects.get(username=user)
        new.status = self.STATUS.copied
        new.task_error = ''
        new.add_info('cloned', self.get_absolute_url())
        new.save()
        # Clone pages
        pages = self.pages_set.all()
        for page in pages:
            new.pages_set.create(
                page=page.page,
                modified=page.modified,
            )
        # Clone annotations
        if options['annotations']:
            anns = self.annotations_set.all()
            for ann in anns:
                new.annotations_set.create(
                    title=ann.title,
                    location=ann.location,
                    page=ann.page,
                    content=ann.content,
                    author=ann.author,
                )
        # Clone editions
        if options['editions']:
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
        if options['zotero']:
            z_tags = Tag.get_tags(self)
            for tag in z_tags:
                new_t = deepcopy(tag)
                new_t.id = None
                new_t.pk = None
                new_t.set_object(new)
#                new_t.save() Not necessary - set_object saves the object
        # Copy collaborators
        if options['collaborators']:
            collabs = self.get_users_with_perms()
            for collab in collabs:
                assign_perm('documents.access_document', collab, new)
        # Copy taggit tags
        if options['tags']:
            t_tags = self.taggit_tags.all()
            for tag in t_tags:
                new.taggit_tags.add(tag.name)
        # Duplicate directories and files
        fs = FileSystemStorage()
        orig_dir_path = self.get_root_path()
        dest_dir_path = new.get_root_path()
        orig_slug = self.slug
        dest_slug = new.slug
        dup_dirs_and_files(
            fs,
            orig_dir_path,
            dest_dir_path,
            orig_slug,
            dest_slug
        )
#        shutil.copytree(old_dir, new_dir)
#        path = os.path.join('media', new_dir)
#        rename_files_recursively(path, old_slug, new_slug)

    class Meta:
        permissions = (
            ('access_document', _('Access Document')),
        )
