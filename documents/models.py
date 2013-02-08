from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth.models import User
from docviewer.models import Document as Docviewer_Document
from guardian.shortcuts import get_users_with_perms


class Reference(models.Model):
    """ Test model for Zotero interaction """
#    def get_annotation(self):
#        raise NotImplementedError("You have to define the get_annotation " +
#                                  "method in the child class!")

#class Book(Reference):
    editorial = models.CharField(
        _('Editorial'), blank=False, null=False, max_length=100,
        help_text=_('Editorial'))

    def __unicode__(self):
        try:
            return u"%s - Editorial de %s (%s): %s" % (
                self.pk, self.document.title, self.document.pk,
                self.editorial)
        except:
            return u"%s - Not Assigned: %s" % (self.pk, self.editorial)

    def get_annotation(self):
        return _("Editorial:") + self.editorial


class Document(Docviewer_Document):
    """ A document with its minimum requiered fields """
    author = models.CharField(
        _('Author'), blank=False, null=False, max_length=100,
        help_text=_('The name of the author of this book'))
    notes = models.TextField(
        _('Notes'), null=True, blank=True,
        help_text=_('Notes of the book'))
    source = models.CharField(
        _('Source'), blank=True, null=False, max_length=50,
        help_text=_('The source of the document'))
    public = models.BooleanField(
        _('Publicly Available'), blank=False, null=False,
        help_text=_('Is this document available to everybody?'))
    owner = models.ForeignKey(User, blank=False, null=False)
    reference = models.OneToOneField(
        Reference, unique=False, blank=False, null=False,
        verbose_name=_('reference'), related_name=_('document'))

    def get_users_with_perms(self):
        return get_users_with_perms(
            self, attach_perms=False, with_superusers=False,
            with_group_users=False).exclude(id=self.owner.id)

    class Meta:
        permissions = (
            ('access_document', _('Access Document')),
        )
