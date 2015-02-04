from django.test import TestCase

from festos.tests.utils import (
    create_user, create_profile, get_user, get_profile, exists_user,
    exists_profile
)


class AccountTest(TestCase):
    def setUp(self):
        self.user = create_user('antonio')
        self.profile = create_profile('antonio')
    
    def test_account_create(self):
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
    
    def test_account_read(self):
        user = get_user('antonio')
        profile = get_profile('antonio')
        
        self.assertIsNotNone(user)
        self.assertIsNotNone(profile)
    
    def test_account_update(self):
        new_email = 'new@email.com'
        self.user.email = new_email
        self.user.save()
        
        self.assertEqual(self.user.email, new_email)
    
    def test_account_delete(self):
        self.user.delete()
        self.profile.delete()
        
        user_exists = exists_user('antonio')
        profile_exists = exists_profile('antonio')
        
        self.assertFalse(user_exists)
        self.assertFalse(profile_exists)
