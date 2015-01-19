import time

from django.conf import settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core.urlresolvers import reverse
from splinter import Browser
from userena.managers import UserenaManager

from utils import create_user, create_profile
from test_signin_up import check_permissions, login


class UploadCloneTest(StaticLiveServerTestCase):
    def setUp(self):
        check_permissions()
        user = create_user('antonio')
        profile = create_profile('antonio')
    
    def test_upload_local_doc(self):
        username = 'antonio'
        password = 'antonio'
        
        browser = Browser()
        login(
            browser,
            self.live_server_url,
            settings.LOGIN_URL,
            username,
            password,
        )
        
        upload_document_partial_url = reverse('documents.views.add_document')
        browser.click_link_by_partial_href(upload_document_partial_url)
        
        browser.choose('source', 'local')
        browser.attach_file('docfile', '/home/antonio/Downloads/995.pdf')
        browser.select('language', 'eng')
        browser.uncheck('public')
        browser.fill('title', 'test')
        browser.fill('notes', 'test notes')
        #TODO Zotero tags
        browser.find_by_value('Add Document').click()
        
        document_list_url = \
            self.live_server_url + reverse('documents.views.list_documents')
        
        self.assertEquals(browser.url, document_list_url)
#        self.assertEquals(profile_link.value, '@{}'.format(username))
        
#        time.sleep(3)
        browser.quit()
    
    def test_upload_dropbox_doc(self):
        pass
    
    def test_edit_doc(self):
        pass
    
    def test_delete_doc(self):
        pass
