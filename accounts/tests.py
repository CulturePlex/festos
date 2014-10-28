from django.contrib.auth.models import User
from django.test import TestCase

from accounts.models import Profile


#class SimpleTest(TestCase):
#    def test_basic_addition(self):
#        """
#        Tests that 1 + 1 always equals 2.
#        """
#        self.assertEqual(1 + 1, 2)

class UserProfileTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username='antonio',
            password='antonio_password',
            email='antonio@email.com',
        )
        self.profile = Profile.objects.create(user=self.user)
    
    def test_user_creation(self):
        self.assertIsNotNone(self.user)
        self.assertIsNotNone(self.user.username)
        self.assertIsNotNone(self.user.password)
        self.assertIsNotNone(self.user.email)
    
    def test_profile_creation(self):
        self.assertIsNotNone(self.profile)
        self.assertEqual(self.profile.user, self.user)
