import uuid

from django.conf import settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core.urlresolvers import reverse
from django.db.models.signals import post_delete, post_save
from selenium.webdriver import ActionChains
from splinter import Browser
from userena.managers import UserenaManager

from documents import fss_utils as fss
from documents.models import Document
from documents.tests import disconnect
from docviewer.models import document_delete, document_save
from utils import create_user, exists_tag, get_document, get_tag
from test_user import check_permissions, login
from test_document import upload, set_site, process_document, get_abs_path


class TagTest(StaticLiveServerTestCase):
    def setUp(self):
        fss.remove_tree(settings.MEDIA_ROOT)
        disconnect(post_save, document_save)
        check_permissions()
        set_site(self.live_server_url)
        
        self.browser = Browser()
        self.browser.visit(self.live_server_url)
        
        login_url = settings.LOGIN_URL
        self.browser.click_link_by_partial_href(login_url)
        
        username = 'antonio'
        password = 'antonio'
        create_user(username)
        login(
            self.browser,
            username,
            password,
        )
        
        upload_url = reverse('documents.views.add_document')
        self.browser.click_link_by_partial_href(upload_url)
        
        source = 'local'
        docfile = get_abs_path('doctest.pdf')
        language = 'eng'
        public = True
        title = 'test'
        notes = 'test notes'
        upload(
            self.browser,
            source,
            docfile,
            language,
            public,
            title,
            notes,
        )
        
        document = get_document(title)
        process_document(document.id)
        self.browser.is_element_not_present_by_value('ready', 10)
        
        tag = 'tag'
        add_tag(
            self.browser,
            tag,
        )
        
        self.tag = tag
        self.tag_obj = get_tag(tag)
    
    def test_add_tag(self):
        tag_exists = exists_tag(self.tag)
        self.assertTrue(tag_exists)
        self.assertEquals(self.tag_obj.name, self.tag)
        
        document_list_url = \
            self.live_server_url + reverse('documents.views.list_documents')
        self.assertEquals(self.browser.url, document_list_url)
        
        tag_span = self.browser.find_by_css('span.taggit_tag')
        self.assertEquals(tag_span.value, self.tag)
        
#        import time; time.sleep(3)
        self.browser.quit()
    
    def test_add_different_tag(self):
        old_tag_num = len(self.browser.find_by_css('span.taggit_tag'))
        
        tag = 'other'
        add_tag(
            self.browser,
            tag,
        )
        
        new_tag_num = len(self.browser.find_by_css('span.taggit_tag'))
        self.assertEquals(new_tag_num, old_tag_num + 1)
        
#        import time; time.sleep(3)
        self.browser.quit()
    
    def test_add_same_tag(self):
        old_tag_num = len(self.browser.find_by_css('span.taggit_tag'))
        
        tag = self.tag
        add_tag(
            self.browser,
            tag,
        )
        
        new_tag_num = len(self.browser.find_by_css('span.taggit_tag'))
        self.assertEquals(new_tag_num, old_tag_num)
        
#        import time; time.sleep(3)
        self.browser.quit()
    
    def test_remove_tag(self):
        old_tag_num = len(self.browser.find_by_css('span.taggit_tag'))
        
        driver = self.browser.driver
        actions = ActionChains(driver)
        tag_link = driver.find_element_by_css_selector('#taggit_tags a')
        actions.move_to_element(tag_link)
        actions.move_by_offset(25, 10)
        actions.click()
        actions.perform()
        
        document_list_url = \
            self.live_server_url + reverse('documents.views.list_documents')
        self.assertEquals(self.browser.url, document_list_url)
        
        new_tag_num = len(self.browser.find_by_css('span.taggit_tag'))
        self.assertEquals(new_tag_num, old_tag_num - 1)
        
#        import time; time.sleep(3)
        self.browser.quit()


def add_tag(browser, tag):
    browser.find_by_css('tr.document-row').mouse_over()
    browser.fill('taggit_tag', tag + '\r')
    import time; time.sleep(1)
