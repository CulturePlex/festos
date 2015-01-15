from django.test import TestCase
from django.contrib.auth.models import User

from accounts.tests import create_user, exists_user, get_user
from documents.models import Document


def create_document(title, username):
    if exists_user(username):
        user = get_user(username)
    else:
        user = create_user(username)
    return Document.objects.create(
        title=title,
        owner=user,
    )

def get_document(title):
    return Document.objects.get(title=title)

def exists_document(title):
    return Document.objects.filter(title=title).exists()


class DocumentTest(TestCase):
    def setUp(self):
        doc = create_document('doc', 'antonio')
    
    def test_document_creation(self):
        user = get_user('antonio')
        doc = get_document('doc')
        
        self.assertIsNotNone(doc)
        self.assertIsNotNone(doc.id)
        self.assertIsNotNone(doc.title)
        self.assertIsNotNone(doc.owner)
        self.assertEqual(doc.user, user)
    
    def test_document_edition(self):
        doc = get_document('doc')
        new_title = 'story'
        doc.title = new_title
        doc.save()
        
        self.assertEqual(doc.title, new_title)
    
    def test_document_deletion(self):
        doc = get_document('doc')
        doc.delete()
        
        self.assertIsNone(user.id)
        
        doc_exists = exists_document('doc')
        
        self.assertFalse(doc_exists)
