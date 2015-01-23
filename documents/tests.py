from django.db.models.signals import post_delete, post_save
from django.test import TestCase
from docviewer.models import document_delete, document_save

from festos.tests.utils import (
    create_user, exists_user, get_user, create_document, exists_document,
    get_document
)


class DocumentTest(TestCase):
    def setUp(self):
        dispatch_uid_ps = recover_dispatch_uid(post_save, document_save)
        post_save.disconnect(document_save, dispatch_uid=dispatch_uid_ps)
        dispatch_uid_pd = recover_dispatch_uid(post_delete, document_delete)
        post_delete.disconnect(document_delete, dispatch_uid=dispatch_uid_pd)
        
        doc = create_document('doc', 'antonio')
    
    def test_document_creation(self):
        user = get_user('antonio')
        doc = get_document('doc')
        
        self.assertIsNotNone(doc)
        self.assertIsNotNone(doc.id)
        self.assertIsNotNone(doc.title)
        self.assertIsNotNone(doc.owner)
        self.assertEqual(doc.owner, user)
    
    def test_document_edition(self):
        doc = get_document('doc')
        new_title = 'story'
        doc.title = new_title
        doc.save()
        
        self.assertEqual(doc.title, new_title)
    
    def test_document_deletion(self):
        doc = get_document('doc')
        doc.delete()
        
        doc_exists = exists_document('doc')
        
        self.assertFalse(doc_exists)


def recover_dispatch_uid(signal, function):
    dispatch_uid = None
    for (ide, weakref) in signal.receivers:
        if weakref() == function:
            dispatch_uid = ide[0]
            break
    return dispatch_uid
