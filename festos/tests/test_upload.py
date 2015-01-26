import os
import uuid

from django.conf import settings
from django.contrib.sites.models import Site
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core.urlresolvers import reverse
from django.db.models.signals import post_delete, post_save
from splinter import Browser
from userena.managers import UserenaManager

from documents import fss_utils as fss
from documents.models import Document
from documents.tests import disconnect
from docviewer.helpers import generate_document
from docviewer.models import document_delete, document_save
from utils import create_user, create_profile
from test_signin_up import check_permissions, login


class UploadTest(StaticLiveServerTestCase):
    def setUp(self):
        fss.remove_tree(settings.MEDIA_ROOT)
        disconnect(post_save, document_save)
        check_permissions()
        set_url_site('localhost:8081')
        
        username = 'antonio'
        password = 'antonio'
        
        user = create_user(username)
        profile = create_profile(password)
        
        self.browser = Browser()
        self.browser.visit(self.live_server_url)
        login(
            self.browser,
            settings.LOGIN_URL,
            username,
            password,
        )
    
    def test_upload_local_doc(self):
        self.browser.visit(self.live_server_url)
        
        source = 'local'
        docfile = '/home/antonio/Downloads/995.pdf'
        language = 'eng'
        public = False
        title = 'test'
        notes = 'test notes'
        
        upload(
            self.browser,
            reverse('documents.views.add_document'),
            source,
            docfile,
            language,
            public,
            title,
            notes,
        )
        
        document_list_url = \
            self.live_server_url + reverse('documents.views.list_documents')
        document_title_xpath = '//*[@id="documents_cell"]/span[1]'
        document_title_elems = self.browser.find_by_xpath(document_title_xpath)
        document_title_first = document_title_elems.first
        profile_xpath = '/html/body/div/div[1]/div/ul[2]/li[4]/a'
        profile_link = self.browser.find_by_xpath(profile_xpath)
        owner_xpath = '/html/body/div/div[2]/table/tbody/tr[1]/td[4]/a'
        owner_link = self.browser.find_by_xpath(owner_xpath)
        
        self.assertEquals(self.browser.url, document_list_url)
        self.assertEquals(document_title_first.value, title)
        self.assertEquals(profile_link.value, owner_link.value)
        
        document_xpath = '/html/body/div/div[2]/table/tbody/tr[1]'
        document_tr = self.browser.find_by_xpath(document_xpath)
        document_id = document_tr['data-id']
        process_document(document_id)
        document = Document.objects.get(id=document_id)
        
        self.browser.is_element_present_by_value('ready', 10)
        
        status_xpath = '/html/body/div/div[2]/table/tbody/tr/td[5]/div'
        status_div = self.browser.find_by_xpath(status_xpath)
        self.assertEquals(status_div.value, 'ready')
        self.assertEquals(document.status, 'ready')
        
#        import time; time.sleep(3)
        self.browser.quit()
        
#    
#    def test_upload_dropbox_doc(self):
#        pass


def set_url_site(url):
    site = Site.objects.get(id=1)
    site.domain = url
    site.name = url
    site.save()


def upload(browser, upload_url, src, docfile, lang, public, title, notes):
    browser.click_link_by_partial_href(upload_url)
    
    browser.choose('source', src)
    browser.attach_file('docfile', docfile)
    browser.select('language', lang)
    if public:
        browser.check('public')
    else:
        browser.uncheck('public')
    browser.fill('title', title)
    browser.fill('notes', notes)
    #ToDo Zotero tags
    browser.find_by_value('Add Document').click()


def process_document(doc_id):
    doc = Document.objects.get(id=doc_id)
    src = os.path.join(settings.MEDIA_ROOT, doc.docfile.name)
    dst = "%s/%s.%s" % (
        doc.get_root_path(),
        doc.slug,
        doc.docfile_basename.split('.')[-1].lower())
    fss.copy_file(src, dst)
    
    generate_document(doc_id)
