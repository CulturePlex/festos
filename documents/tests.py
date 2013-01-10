"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from models import Document
from settings import PROJECT_ROOT
from os.path import join
from os import listdir



class DocumentTestCase(TestCase):
    def test_upload_examples(self):
        path = join(PROJECT_ROOT,tests)
        self.assertEqual(
          Document.objects.upload_examples(path), 
          len (listdir(path)))

