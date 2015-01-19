import time

from django.conf import settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core.urlresolvers import reverse
#from django.test import LiveServerTestCase
#from django.test.utils import override_settings
from splinter import Browser
from userena.managers import UserenaManager

from utils import create_user, create_profile


class SignInUpTest(StaticLiveServerTestCase):
#    @override_settings(DEBUG=True)
#    
    def setUp(self):
        check_permissions()
        user = create_user('antonio')
        profile = create_profile('antonio')
    
    def test_signin(self):
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
        
        profile_xpath = '/html/body/div/div[1]/div/ul[2]/li[4]/a'
        profile_link = browser.find_by_xpath(profile_xpath)
        document_list_url = \
            self.live_server_url + reverse('documents.views.list_documents')
        
        self.assertEquals(browser.url, document_list_url)
        self.assertEquals(profile_link.value, '@{}'.format(username))
        
#        time.sleep(3)
        browser.quit()

    def test_signup(self):
        username = 'andres'
        password = 'andres'
        email = 'andres@email.com'
        
        browser = Browser()
        signup(
            browser,
            self.live_server_url,
            settings.SIGNUP_URL,
            username,
            password,
            email,
        )
        
        profile_xpath = '/html/body/div/div[1]/div/ul[2]/li[4]/a'
        profile_link = browser.find_by_xpath(profile_xpath)
        document_list_url = \
            self.live_server_url + reverse('documents.views.list_documents')
        
        self.assertEquals(browser.url, document_list_url)
        self.assertEquals(profile_link.value, '@{}'.format(username))
        
#        time.sleep(3)
        browser.quit()


def check_permissions():
    um = UserenaManager()
    um.check_permissions()


def login(browser, global_url, login_url, username, password):
    browser.visit(global_url)
    browser.click_link_by_partial_href(login_url)
    
    browser.find_by_id('id_identification').type(username)
    browser.find_by_id('id_password').type(password)
    browser.find_by_value('Signin').click()


def signup(browser, global_url, signup_url, username, password, email):
    browser.visit(global_url)
    browser.click_link_by_partial_href(signup_url)
    
    browser.find_by_id('id_username').type(username)
    browser.find_by_id('id_email').type(email)
    browser.find_by_id('id_password1').type(password)
    browser.find_by_id('id_password2').type(password)
    browser.find_by_value('Sign Up').click()
