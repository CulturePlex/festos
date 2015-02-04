import itertools
import os
import uuid
from urlparse import urlsplit

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
from utils import create_user, create_profile, get_document
from test_signin_up import check_permissions, login


class DocTest(StaticLiveServerTestCase):
    def setUp(self):
        fss.remove_tree(settings.MEDIA_ROOT)
        disconnect(post_save, document_save)
        check_permissions()
        set_site(self.live_server_url)
        
        username = 'antonio'
        password = 'antonio'
        create_user(username)
        create_profile(username)
        
        self.browser = Browser()
        self.browser.visit(self.live_server_url)
        login(
            self.browser,
            settings.LOGIN_URL,
            username,
            password,
        )
        
        source = 'local'
        docfile = get_abs_path('doctest.pdf')
        language = 'eng'
        public = True
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
        
        document = get_document(title)
        process_document(document.id)
        self.browser.is_element_present_by_value('ready', 10)
    
    def test_upload_local(self):
        self.browser.visit(self.live_server_url)
        
        source = 'local'
        docfile = get_abs_path('doctest.pdf')
        language = 'eng'
        public = True
        title = 'other'
        notes = 'other notes'
        
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
        
        document = get_document(title)
        
        self.assertEquals(document.public, public)
        self.assertEquals(document.title, title)
        self.assertEquals(document.notes, notes)
        
        document_list_url = \
            self.live_server_url + reverse('documents.views.list_documents')
        
        self.assertEquals(self.browser.url, document_list_url)
        
        process_document(document.id)
        document = get_document(title) # status and page_count have changed
        self.browser.is_element_present_by_value('ready', 10)
        
        document_xpath = '/html/body/div/div[2]/table/tbody/tr[1]'
        document_tr = self.browser.find_by_xpath(document_xpath)
        document_id = document_tr['data-id']
        document_title_xpath = '//*[@id="documents_cell"]/span[1]'
        document_title_elems = self.browser.find_by_xpath(document_title_xpath)
        document_title_first = document_title_elems.first
        profile_xpath = '/html/body/div/div[1]/div/ul[2]/li[4]/a'
        profile_link = self.browser.find_by_xpath(profile_xpath)
        owner_xpath = '/html/body/div/div[2]/table/tbody/tr[1]/td[4]/a'
        owner_link = self.browser.find_by_xpath(owner_xpath)
        status_xpath = '/html/body/div/div[2]/table/tbody/tr/td[5]/div'
        status_div = self.browser.find_by_xpath(status_xpath)
        numpages_xpath = '/html/body/div/div[2]/table/tbody/tr[1]/td[6]/div'
        numpages_div = self.browser.find_by_xpath(numpages_xpath)
        privacy_icon_xpath = '//*[@id="privacy"]/i'
        privacy_icon_elems = self.browser.find_by_xpath(privacy_icon_xpath)
        privacy_icon_first = privacy_icon_elems.first
        
        self.assertEquals(int(document_id), document.id)
        self.assertEquals(document_title_first.value, title)
        self.assertEquals(profile_link.value, owner_link.value)
        self.assertEquals(status_div.value, 'ready')
        self.assertEquals(document.status, 'ready')
        self.assertEquals(int(numpages_div.value), document.page_count)
        self.assertTrue(privacy_icon_first.has_class('icon-eye-open'))
        
        structure = create_structure(document)
        root_path = document.get_root_path()
        dirs = fss.listdir(root_path)[0]
        files = fss.listdir(root_path)[1]
        for d in dirs:
            dir_path = os.path.join(root_path, d)
            for f in structure['dirs'][d]:
                self.assertIn(f, fss.listdir(dir_path)[1])
        for f in structure['files']:
            self.assertIn(f, fss.listdir(root_path)[1])
        
#        import time; time.sleep(3)
        self.browser.quit()
#    
#    def test_upload_dropbox(self):
#        pass
    
#    def test_access_viewer(self):
#        pass
#        #Just check we have access to docviewer
    
    def test_edit(self):
        self.browser.visit(self.live_server_url)
        
        public = True
        title = 'new title'
        notes = 'new notes'
        
        edit(
            self.browser,
            reverse('documents.views.list_documents'),
            public,
            title,
            notes,
        )
        
        document_list_url = \
            self.live_server_url + reverse('documents.views.list_documents')
        self.assertEquals(self.browser.url, document_list_url)
        
        document_xpath = '/html/body/div/div[2]/table/tbody/tr[1]'
        document_tr = self.browser.find_by_xpath(document_xpath)
        document_id = document_tr['data-id']
        document = Document.objects.get(id=document_id)
        
        self.assertEquals(document.public, public)
        self.assertEquals(document.title, title)
        self.assertEquals(document.notes, notes)
        
        document_title_xpath = '//*[@id="documents_cell"]/span[1]'
        document_title_elems = self.browser.find_by_xpath(document_title_xpath)
        document_title_first = document_title_elems.first
        privacy_icon_xpath = '//*[@id="privacy"]/i'
        privacy_icon_elems = self.browser.find_by_xpath(privacy_icon_xpath)
        privacy_icon_first = privacy_icon_elems.first
        
        self.assertEquals(document_title_first.value, title)
        self.assertTrue(privacy_icon_first.has_class('icon-eye-open'))
        
#        import time; time.sleep(3)
        self.browser.quit()


def set_site(url):
    dom = urlsplit(url).netloc
    site = Site.objects.get_current()
    site.domain = dom
    site.name = dom
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


def create_structure(document):
    def create_file_list(document):
        file_tuples = [(
                document.slug + '_' + str(p) + '.txt',
                document.slug + '_' + str(p) + '-' + '0' * 20 + '.txt',
            )
            for p in range(1, document.page_count + 1)
        ]
        files = [f for f in itertools.chain(*file_tuples)]
        return files
    
    def create_dir_list(document):
        files = [
            document.slug + '_' + str(p) + '.png'
            for p in range(1, document.page_count + 1)]
        dirs = {'large': files, 'normal': files, 'small': files}
        return dirs
    
    structure = {
        'files': create_file_list(document),
        'dirs': create_dir_list(document),
    }
    return structure


def get_abs_path(filename):
    return os.path.join(
        settings.PROJECT_ROOT,
        'festos',
        'tests',
        'files',
        filename
    )
