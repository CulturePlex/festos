from django.test import TestCase

from festos.tests.utils import (
    create_user, create_profile, get_user, get_profile, exists_user,
    exists_profile
)


class AccountTest(TestCase):
    def setUp(self):
        self.username = 'antonio'
        self.user = create_user(self.username)
        self.profile = create_profile(self.username)
    
    def test_account_create(self):
        self.assertIsNotNone(self.user)
        self.assertIsNotNone(self.user.id)
        self.assertIsNotNone(self.user.username)
        self.assertEqual(self.user.username, self.username)
        self.assertIsNotNone(self.user.password)
        self.assertIsNotNone(self.user.email)
        self.assertIsNotNone(self.profile)
        self.assertIsNotNone(self.profile.id)
        self.assertEqual(self.profile.user, self.user)
    
    def test_account_read(self):
        user = get_user(self.username)
        profile = get_profile(self.username)
        
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
        
        user_exists = exists_user(self.username)
        profile_exists = exists_profile(self.username)
        
        self.assertFalse(user_exists)
        self.assertFalse(profile_exists)
