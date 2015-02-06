from django.conf import settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core.urlresolvers import reverse
#from django.test import LiveServerTestCase
from splinter import Browser
from userena.managers import UserenaManager

from utils import create_user, exists_user


class UserTest(StaticLiveServerTestCase):
    def setUp(self):
        check_permissions()
        
        self.username = 'antonio'
        create_user(self.username)
        
        self.browser = Browser()

    def test_signup(self):
        self.browser.visit(self.live_server_url)
        
        username = 'andres'
        password = 'andres'
        email = 'andres@email.com'
        
        signup(
            self.browser,
            settings.SIGNUP_URL,
            username,
            password,
            email,
        )
        
        user_exists = exists_user(username)
        
        self.assertTrue(user_exists)
        
        profile_xpath = '/html/body/div/div[1]/div/ul[2]/li[4]/a'
        profile_link = self.browser.find_by_xpath(profile_xpath)
        document_list_url = \
            self.live_server_url + reverse('documents.views.list_documents')
        
        self.assertEquals(self.browser.url, document_list_url)
        self.assertEquals(profile_link.value, '@{}'.format(username))
        
#        import time; time.sleep(3)
        self.browser.quit()
    
    def test_signin(self):
        self.browser.visit(self.live_server_url)
        
        username = self.username
        password = self.username
        
        login(
            self.browser,
            settings.LOGIN_URL,
            username,
            password,
        )
        
        profile_xpath = '/html/body/div/div[1]/div/ul[2]/li[4]/a'
        profile_link = self.browser.find_by_xpath(profile_xpath)
        document_list_url = \
            self.live_server_url + reverse('documents.views.list_documents')
        
        self.assertEquals(self.browser.url, document_list_url)
        self.assertEquals(profile_link.value, '@{}'.format(username))
        
#        import time; time.sleep(3)
        self.browser.quit()


def check_permissions():
    um = UserenaManager()
    um.check_permissions()


def signup(browser, signup_url, username, password, email):
    browser.click_link_by_partial_href(signup_url)
    
    browser.find_by_id('id_username').type(username)
    browser.find_by_id('id_email').type(email)
    browser.find_by_id('id_password1').type(password)
    browser.find_by_id('id_password2').type(password)
    browser.find_by_value('Sign Up').click()


def login(browser, login_url, username, password):
    browser.click_link_by_partial_href(login_url)
    
    browser.find_by_id('id_identification').type(username)
    browser.find_by_id('id_password').type(password)
    browser.find_by_value('Signin').click()
