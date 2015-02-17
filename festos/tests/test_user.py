from django.conf import settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core.urlresolvers import reverse
#from django.test import LiveServerTestCase
from splinter import Browser
from userena.managers import UserenaManager

from utils import create_user, exists_user, get_user


class UserTest(StaticLiveServerTestCase):
    def setUp(self):
        check_permissions()
        self.username = 'antonio'
        create_user(self.username)
        
        self.browser = Browser()
        self.browser.visit(self.live_server_url)

    def test_signup(self):
        signup_url = settings.SIGNUP_URL
        self.browser.click_link_by_partial_href(signup_url)
        
        username = 'andres'
        password = 'andres'
        email = 'andres@email.com'
        signup(
            self.browser,
            username,
            password,
            email,
        )
        
        user_exists = exists_user(username)
        self.assertTrue(user_exists)
        
        user = get_user(username)
        self.assertEquals(user.username, username)
        #self.assertEquals(user.password, password)
        self.assertEquals(user.email, email)
        
        document_list_url = \
            self.live_server_url + reverse('documents.views.list_documents')
        self.assertEquals(self.browser.url, document_list_url)
        
        profile_xpath = '/html/body/div/div[1]/div/ul[2]/li[4]/a'
        profile_link = self.browser.find_by_xpath(profile_xpath)
        self.assertEquals(profile_link.value, '@{}'.format(username))
        
#        import time; time.sleep(3)
        self.browser.quit()
    
    def test_signin(self):
        login_url = settings.LOGIN_URL
        self.browser.click_link_by_partial_href(login_url)
        
        username = self.username
        password = self.username
        login(
            self.browser,
            username,
            password,
        )
        
        document_list_url = \
            self.live_server_url + reverse('documents.views.list_documents')
        self.assertEquals(self.browser.url, document_list_url)
        
        profile_xpath = '/html/body/div/div[1]/div/ul[2]/li[4]/a'
        profile_link = self.browser.find_by_xpath(profile_xpath)
        self.assertEquals(profile_link.value, '@{}'.format(username))
        
#        import time; time.sleep(3)
        self.browser.quit()


def check_permissions():
    um = UserenaManager()
    um.check_permissions()


def signup(browser, username, password, email):
    browser.fill('username', username)
    browser.fill('email', email)
    browser.fill('password1', password)
    browser.fill('password2', password)
    browser.find_by_value('Sign Up').click()


def login(browser,  username, password):
    browser.fill('identification', username)
    browser.fill('password', password)
    browser.find_by_value('Signin').click()
