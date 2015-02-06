from django.db.models.signals import post_delete, post_save
from django.test import TestCase
from docviewer.models import document_delete, document_save

from festos.tests.utils import (
    create_user, exists_user, get_user, create_document, exists_document,
    get_document
)


class DocumentTest(TestCase):
    def setUp(self):
        disconnect(post_save, document_save)
        disconnect(post_delete, document_delete)
        
        self.username = 'antonio'
        self.title = 'test'
        self.user = create_user(self.username)
        self.document = create_document(self.title, self.username)
    
    def test_document_create(self):
        self.assertIsNotNone(self.document)
        self.assertIsNotNone(self.document.id)
        self.assertIsNotNone(self.document.title)
        self.assertEqual(self.document.title, self.title)
        self.assertIsNotNone(self.document.owner)
        self.assertEqual(self.document.owner, self.user)
    
    def test_document_read(self):
        doc = get_document(self.title)
        
        self.assertIsNotNone(doc)
    
    def test_document_update(self):
        new_title = 'story'
        self.document.title = new_title
        self.document.save()
        
        self.assertEqual(self.document.title, new_title)
    
    def test_document_delete(self):
        self.document.delete()
        
        doc_exists = exists_document(self.title)
        
        self.assertFalse(doc_exists)


def disconnect(signal, function):
    def recover_dispatch_uid(signal, function):
        dispatch_uid = None
        for (ide, weakref) in signal.receivers:
            if weakref() == function:
                dispatch_uid = ide[0]
                break
        return dispatch_uid
    
    dispatch_uid = recover_dispatch_uid(signal, function)
    signal.disconnect(function, dispatch_uid=dispatch_uid)
