#import uuid

#from django.conf import settings
#from django.contrib.staticfiles.testing import StaticLiveServerTestCase
#from django.core.urlresolvers import reverse
#from django.db.models.signals import post_delete, post_save
#from splinter import Browser
#from userena.managers import UserenaManager

#from documents import fss_utils as fss
#from documents.models import Document
#from documents.tests import disconnect
#from docviewer.models import document_delete, document_save
#from utils import create_user, create_profile, exists_tag
#from test_signin_up import check_permissions, login
#from test_upload import upload, set_url_site, process_document


#class EditTest(StaticLiveServerTestCase):
#    def setUp(self):
#        fss.remove_tree(settings.MEDIA_ROOT)
#        disconnect(post_save, document_save)
##        disconnect(post_delete, document_delete)
#        check_permissions()
#        set_url_site('localhost:8081')
#        
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
#        document_xpath = '/html/body/div/div[2]/table/tbody/tr[1]'
#        document_tr = self.browser.find_by_xpath(document_xpath)
#        document_id = document_tr['data-id']
#        process_document(document_id)
#        
#        self.browser.is_element_present_by_value('ready', 10)
#    
#    def test_add_tag(self):
#        self.browser.visit(self.live_server_url)
#        
#        tag = 'tag'
#        
#        add_tag(
#            self.browser,
#            reverse('documents.views.list_documents'),
#            tag,
#        )
#        
#        document_list_url = \
#            self.live_server_url + reverse('documents.views.list_documents')
#        self.assertEquals(self.browser.url, document_list_url)
#        
#        last_tag_elem = b.find_by_css('span.taggit_tag').last
#        last_tag_text = last_tag_elem.text
#        
#        
##        document_xpath = '/html/body/div/div[2]/table/tbody/tr[1]'
##        document_tr = self.browser.find_by_xpath(document_xpath)
##        document_id = document_tr['data-id']
##        document = Document.objects.get(id=document_id)
##        
##        self.assertEquals(document.public, public)
##        self.assertEquals(document.title, title)
##        self.assertEquals(document.notes, notes)
##        
##        document_title_xpath = '//*[@id="documents_cell"]/span[1]'
##        document_title_elems = self.browser.find_by_xpath(document_title_xpath)
##        document_title_first = document_title_elems.first
##        privacy_icon_xpath = '//*[@id="privacy"]/i'
##        privacy_icon_elems = self.browser.find_by_xpath(privacy_icon_xpath)
##        privacy_icon_first = privacy_icon_elems.first
##        
##        self.assertEquals(document_title_first.value, title)
##        self.assertTrue(privacy_icon_first.has_class('icon-eye-open'))
##        
###        import time; time.sleep(3)
##        self.browser.quit()


#def edit(browser, list_url, public, title, notes):
#    browser.click_link_by_partial_href(list_url)
#    
#    edit_xpath = '/html/body/div/div[2]/table/tbody/tr[1]/td[7]/a[3]/i'
#    edit_icon = browser.find_by_xpath(edit_xpath)
#    edit_icon.click()
#    
#    if public:
#        browser.check('public')
#    else:
#        browser.uncheck('public')
#    browser.fill('title', title)
#    browser.fill('notes', notes)
#    #ToDo Zotero tags
#    browser.find_by_value('Save Document').click()


#def add_tag(browser, list_url, tag):
#    browser.click_link_by_partial_href(list_url)
#    
#    browser.find_by_css('tr.document-row').first.mouse_over()
#    browser.fill('taggit_tag', tag + '\r')
