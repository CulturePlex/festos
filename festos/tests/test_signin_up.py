from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
#from django.test import TestCase
from django.test import LiveServerTestCase
from splinter import Browser


class BrowserTest(LiveServerTestCase):
    def test_signin(self):
        username = 'festos'
        password = 'festos'
        
        browser = Browser()
        browser.visit(self.live_server_url)
        browser.click_link_by_partial_href(settings.LOGIN_URL)
        
        browser.find_by_id('id_identification').type(username)
        browser.find_by_id('id_password').type(password)
        browser.find_by_value('Signin').click()
        
        profile_xpath = '/html/body/div/div[1]/div/ul[2]/li[4]/a'
        profile_link = browser.find_by_xpath(profile_xpath)
        document_list_url = \
            self.live_server_url + reverse('documents.views.list_documents')
        
        self.assertEquals(browser.url, document_list_url)
        self.assertEquals(profile_link.value, '@{}'.format(username))

        browser.quit()

    def test_signup(self):
        username = 'antonio'
        password = 'antonio'
        email = 'antonio@email.com'
        
        browser = Browser()
        browser.visit(self.live_server_url)
        browser.click_link_by_partial_href(settings.SIGNUP_URL)
        
        browser.find_by_id('id_username').type(username)
        browser.find_by_id('id_email').type(email)
        browser.find_by_id('id_password1').type(password)
        browser.find_by_id('id_password2').type(password)
        browser.find_by_value('Sign Up').click()
        
        profile_xpath = '/html/body/div/div[1]/div/ul[2]/li[4]/a'
        profile_link = browser.find_by_xpath(profile_xpath)
        document_list_url = \
            self.live_server_url + reverse('documents.views.list_documents')
        
        self.assertEquals(browser.url, document_list_url)
        self.assertEquals(profile_link.value, '@{}'.format(username))

        browser.quit()
