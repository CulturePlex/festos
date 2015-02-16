import itertools
import os
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
from utils import create_user, get_document, exists_document
from test_user import check_permissions, login


class DocTest(StaticLiveServerTestCase):
    def setUp(self):
        fss.remove_tree(settings.MEDIA_ROOT)
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
        
        self.browser.is_element_not_present_by_value('ready', 10)
        
        self.public = public
        self.title = title
        self.notes = notes
        self.document = get_document(title)
    
    def test_upload_doc_local(self): #Create
        document_exists = exists_document(self.title)
        self.assertTrue(document_exists)
        self.assertEquals(self.document.public, self.public)
        self.assertEquals(self.document.title, self.title)
        self.assertEquals(self.document.notes, self.notes)
        
        document_list_url = \
            self.live_server_url + reverse('documents.views.list_documents')
        self.assertEquals(self.browser.url, document_list_url)
        
        document_xpath = '/html/body/div/div[2]/table/tbody/tr[1]'
        document_tr = self.browser.find_by_xpath(document_xpath)
        document_id = document_tr['data-id']
        self.assertEquals(int(document_id), self.document.id)
        
        document_title_xpath = '//*[@id="documents_cell"]/span[1]'
        document_title = self.browser.find_by_xpath(document_title_xpath)
        self.assertEquals(document_title.value, self.title)
        
        profile_xpath = '/html/body/div/div[1]/div/ul[2]/li[4]/a'
        profile_link = self.browser.find_by_xpath(profile_xpath)
        owner_xpath = '/html/body/div/div[2]/table/tbody/tr[1]/td[4]/a'
        owner_link = self.browser.find_by_xpath(owner_xpath)
        self.assertEquals(profile_link.value, owner_link.value)
        
        status_xpath = '/html/body/div/div[2]/table/tbody/tr/td[5]/div'
        status_div = self.browser.find_by_xpath(status_xpath)
        self.assertEquals(status_div.value, self.document.status)
        
        numpages_xpath = '/html/body/div/div[2]/table/tbody/tr[1]/td[6]/div'
        numpages_div = self.browser.find_by_xpath(numpages_xpath)
        self.assertEquals(int(numpages_div.value), self.document.page_count)
        
        privacy_icon_xpath = '//*[@id="privacy"]/i'
        privacy_icon = self.browser.find_by_xpath(privacy_icon_xpath)
        self.assertTrue(privacy_icon.has_class('icon-eye-open'))
        
        structure = create_structure(self.document)
        root_path = self.document.get_root_path()
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
#    def test_upload_doc_dropbox(self): #Create
#        pass
    
    def test_view_doc(self): #Read
        link_title_xpath = '//*[@id="documents_cell"]/span[1]/a'
        self.browser.find_by_xpath(link_title_xpath).click()
        viewer_title_xpath = (
            '//*[@id="documentviewer-container"]'
            '/div/div[1]/div[1]/div[1]/div[2]/h4/a'
        )
        viewer_title = self.browser.find_by_xpath(viewer_title_xpath)
        self.assertEquals(viewer_title.value, self.title)
        
#        import time; time.sleep(3)
        self.browser.quit()
    
    def test_edit_doc(self): #Update
        edit_xpath = '/html/body/div/div[2]/table/tbody/tr[1]/td[7]/a[3]/i'
        self.browser.find_by_xpath(edit_xpath).click()
        
        public = False
        title = 'new title'
        notes = 'new notes'
        edit(
            self.browser,
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
        
        document_title_xpath = '//*[@id="documents_cell"]/span[1]'
        document_title = self.browser.find_by_xpath(document_title_xpath)
        self.assertEquals(document_title.value, title)
        
        privacy_icon_xpath = '//*[@id="privacy"]/i'
        privacy_icon = self.browser.find_by_xpath(privacy_icon_xpath)
        self.assertTrue(privacy_icon.has_class('icon-eye-close'))
        
#        import time; time.sleep(3)
        self.browser.quit()
    
    def test_remove_doc(self): #Delete
        old_doc_num = len(self.browser.find_by_css('tr.document-row'))
        
        remove_xpath = '//*[@id="remove"]/i'
        self.browser.find_by_xpath(remove_xpath).click()
        confirm_xpath = '//*[@id="confirm-remove"]/i'
        self.browser.find_by_xpath(confirm_xpath).click()
        
        document_list_url = \
            self.live_server_url + reverse('documents.views.list_documents')
        self.assertEquals(self.browser.url, document_list_url)
        
        new_doc_num = len(self.browser.find_by_css('tr.document-row'))
        self.assertEquals(new_doc_num, old_doc_num - 1)
        
#        import time; time.sleep(3)
        self.browser.quit()


def set_site(url):
    dom = urlsplit(url).netloc
    site = Site.objects.get_current()
    site.domain = dom
    site.name = dom
    site.save()


def upload(browser, src, docfile, lang, public, title, notes):
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


def edit(browser, public, title, notes):
    if public:
        browser.check('public')
    else:
        browser.uncheck('public')
    browser.fill('title', title)
    browser.fill('notes', notes)
    #ToDo Zotero tags
    browser.find_by_value('Save Document').click()
