from django.test import TestCase

from festos.tests.utils import (
    create_user, create_profile, get_user, get_profile, exists_user,
    exists_profile
)


class AccountTest(TestCase):
    def setUp(self):
        user = create_user('antonio')
        profile = create_profile('antonio')
    
    def test_account_creation(self):
        user = create_user('andres')
        profile = create_profile(user)
        
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
        
        user_exists = exists_user('antonio')
        profile_exists = exists_profile('antonio')
        
        self.assertFalse(user_exists)
        self.assertFalse(profile_exists)
