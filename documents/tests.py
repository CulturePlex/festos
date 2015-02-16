import uuid

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
        
        connect(post_save, document_save)
    
    def test_document_read(self):
        doc = get_document(self.title)
        self.assertIsNotNone(doc)
        
        connect(post_save, document_save)
    
    def test_document_update(self):
        new_title = 'story'
        self.document.title = new_title
        self.document.save()
        self.assertEqual(self.document.title, new_title)
        
        connect(post_save, document_save)
    
    def test_document_delete(self):
        disconnect(post_delete, document_delete)
        
        self.document.delete()
        doc_exists = exists_document(self.title)
        self.assertFalse(doc_exists)
        
        connect(post_delete, document_delete)
        connect(post_save, document_save)


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


def connect(signal, function):
    dispatch_uid = str(uuid.uuid1())
    signal.connect(function, dispatch_uid=dispatch_uid)
