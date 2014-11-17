from django.contrib.auth.models import User
from django.test import TestCase

from accounts.models import Profile


#class SimpleTest(TestCase):
#    def test_basic_addition(self):
#        """
#        Tests that 1 + 1 always equals 2.
#        """
#        self.assertEqual(1 + 1, 2)

def create_user(username):
    return User.objects.create(
        username=username,
        password=username,
        email='{}@email.com'.format(username),
    )

def create_profile(user):
    return Profile.objects.create(user=user)

def get_user(username):
    return User.objects.get(username=username)

def get_profile(username):
    return Profile.objects.get(user__username=username)

def exists_user(username):
    return User.objects.filter(username=username).exists()

def exists_profile(username):
    return Profile.objects.filter(user__username=username).exists()


class AccountTest(TestCase):
    def setUp(self):
        user = create_user('antonio')
        profile = create_profile(user)
    
    def test_account_creation(self):
        user = get_user('antonio')
        profile = get_profile('antonio')
        
        self.assertIsNotNone(user)
        self.assertIsNotNone(user.id)
        self.assertIsNotNone(user.username)
        self.assertIsNotNone(user.password)
        self.assertIsNotNone(user.email)
        self.assertIsNotNone(profile)
        self.assertIsNotNone(profile.id)
        self.assertEqual(profile.user, user)
    
    def test_account_edition(self):
        user = get_user('antonio')
        profile = get_profile('antonio')
        new_email = 'new@email.com'
        user.email = new_email
        user.save()
        
        self.assertEqual(profile.user.email, new_email)
    
    def test_account_deletion(self):
        user = get_user('antonio')
        profile = get_profile('antonio')
        user.delete()
        profile.delete()
        
        self.assertIsNone(user.id)
        self.assertIsNone(profile.id)
        
        user_exists = exists_user('antonio')
        profile_exists = exists_profile('antonio')
        
        self.assertFalse(user_exists)
        self.assertFalse(profile_exists)


from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.test import TestCase
from splinter import Browser


BASE_URL = 'http://{}'.format(Site.objects.get_current().domain)


class BrowserTest(TestCase):
    def test_signin(self):
        username = 'festos'
        password = 'festos'
        
        browser = Browser()
        browser.visit(BASE_URL)
        browser.click_link_by_partial_href(settings.LOGIN_URL)
        
        browser.find_by_id('id_identification').type(username)
        browser.find_by_id('id_password').type(password)
        browser.find_by_value('Signin').click()
        
        profile_xpath = '/html/body/div/div[1]/div/ul[2]/li[4]/a'
        profile_link = browser.find_by_xpath(profile_xpath)
        document_list_link = \
            BASE_URL + reverse('documents.views.list_documents')
        
        self.assertEquals(browser.url, document_list_link)
        self.assertEquals(profile_link.value, '@{}'.format(username))

#        browser.quit()

    def test_signup(self):
        username = 'antonio'
        password = 'antonio'
        email = 'antonio@email.com'
        
        browser = Browser()
        browser.visit(BASE_URL)
        browser.click_link_by_partial_href(settings.SIGNUP_URL)
        
        browser.find_by_id('id_username').type(username)
        browser.find_by_id('id_email').type(email)
        browser.find_by_id('id_password1').type(password)
        browser.find_by_id('id_password2').type(password)
        browser.find_by_value('Sign Up').click()
        
        profile_xpath = '/html/body/div/div[1]/div/ul[2]/li[4]/a'
        profile_link = browser.find_by_xpath(profile_xpath)
        document_list_link = \
            BASE_URL + reverse('documents.views.list_documents')
        
        self.assertEquals(browser.url, document_list_link)
        self.assertEquals(profile_link.value, '@{}'.format(username))

#        browser.quit()
