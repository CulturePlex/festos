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
from test_document import upload, set_site, get_abs_path


class SearchTest(StaticLiveServerTestCase):
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
        
        self.title = title
        import time; time.sleep(1)
    
    def test_search_title(self):
        self.browser.visit(self.live_server_url)
        
        title = 'test'
        
        driver = self.browser.driver
        actions = ActionChains(driver)
        searchbar_xpath = '//*[@id="search"]/div/div/div[2]'
        searchbar_div = driver.find_element_by_xpath(searchbar_xpath)
        actions.move_to_element(searchbar_div)
        actions.click()
        actions.perform()
        
        menu_title_xpath = '/html/body/ul/li[4]/a'
        menu_title = self.browser.find_by_xpath(menu_title_xpath)
        menu_title.click()
        input_title_xpath = \
            '//*[@id="search"]/div/div/div[2]/div[2]/div[2]/input'
        input_title = self.browser.find_by_xpath(input_title_xpath)
        input_title.type(title + '\r')
        
        search_list_url = \
            self.live_server_url + '/?title=' + title + '&'
        self.assertEquals(self.browser.url, search_list_url)
        
        summary_xpath = '/html/body/div/div[2]/p/small'
        summary = self.browser.find_by_xpath(summary_xpath)
        self.assertEquals(summary.value, '1 documents found')
        
        document_img_xpath = '/html/body/div/div[2]/ul/li/a/img'
        document_img = self.browser.find_by_xpath(document_img_xpath).click()
        viewer_title_xpath = (
            '//*[@id="documentviewer-container"]'
            '/div/div[1]/div[1]/div[1]/div[2]/h4/a'
        )
        viewer_title = self.browser.find_by_xpath(viewer_title_xpath)
        self.assertEquals(viewer_title.value, self.title)
        
#        import time; time.sleep(3)
        self.browser.quit()
    
    def test_search_text(self):
        self.browser.visit(self.live_server_url)
        
        text = 'download'
        
        driver = self.browser.driver
        actions = ActionChains(driver)
        searchbar_xpath = '//*[@id="search"]/div/div/div[2]'
        searchbar_div = driver.find_element_by_xpath(searchbar_xpath)
        actions.move_to_element(searchbar_div)
        actions.click()
        actions.perform()
        
        menu_text_xpath = '/html/body/ul/li[3]/a'
        menu_text = self.browser.find_by_xpath(menu_text_xpath)
        menu_text.click()
        input_text_xpath = \
            '//*[@id="search"]/div/div/div[2]/div[2]/div[2]/input'
        input_text = self.browser.find_by_xpath(input_text_xpath)
        input_text.type(text + '\r')
        
        search_list_url = \
            self.live_server_url + '/?q=' + text + '&'
        self.assertEquals(self.browser.url, search_list_url)
        
        summary_xpath = '/html/body/div/div[2]/p/small'
        summary = self.browser.find_by_xpath(summary_xpath)
        self.assertEquals(summary.value, '1 documents found')
        
        page_xpath = '/html/body/div/div[2]/ul/li[1]/div[2]/div/div[2]/a/div'
        page_div = self.browser.find_by_xpath(page_xpath)
        self.assertIn(text, page_div.value)
        
        document_img_xpath = '/html/body/div/div[2]/ul/li/a/img'
        document_img = self.browser.find_by_xpath(document_img_xpath).click()
        viewer_title_xpath = (
            '//*[@id="documentviewer-container"]'
            '/div/div[1]/div[1]/div[1]/div[2]/h4/a'
        )
        viewer_title = self.browser.find_by_xpath(viewer_title_xpath)
        self.assertEquals(viewer_title.value, self.title)
        
#        import time; time.sleep(3)
        self.browser.quit()
