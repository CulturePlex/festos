import uuid

from django.conf import settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core.urlresolvers import reverse
from django.db.models.signals import post_delete, post_save
from splinter import Browser
from userena.managers import UserenaManager

from documents import fss_utils as fss
from docviewer.models import document_delete, document_save
from utils import create_user, create_profile
from test_signin_up import check_permissions, login
from test_upload import upload


# editar titulo o notas, editar notas, editar text, editar tags, editar todo!!

#class UploadEditTest(StaticLiveServerTestCase):
#    def setUp(self):
#        fss.remove_tree(settings.MEDIA_ROOT)
#        post_save.connect(document_save, dispatch_uid=str(uuid.uuid1()))
#        post_delete.connect(document_delete)
#        
#        check_permissions()
#        username = 'antonio'
#        password = 'antonio'
#        
#        user = create_user(username)
#        profile = create_profile(password)
#        
#        self.browser = Browser()
#        self.browser.visit(self.live_server_url)
#        login(
#            self.browser,
#            settings.LOGIN_URL,
#            username,
#            password,
#        )
#        
#        source = 'local'
#        docfile = '/home/antonio/Downloads/995.pdf'
#        language = 'eng'
#        public = False
#        title = 'test'
#        notes = 'test notes'
#        
#        upload(
#            self.browser,
#            reverse('documents.views.add_document'),
#            source,
#            docfile,
#            language,
#            public,
#            title,
#            notes,
#        )
#    
#    def test_edit_doc(self):
#        self.browser.quit()
#        print "EDIT"
