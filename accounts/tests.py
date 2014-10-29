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
        password='{}_password'.format(username),
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
