from django.test import TestCase
from django.contrib.auth.models import User
from user.models import Profile
from django.core.files.base import ContentFile

# Create your tests here.
class UserTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_user(id=30,username='matinaa', email='matinaaaa@gmail.com', password='p1234567')

    def test_user_name(self):
        user = User.objects.get(id=30)
        self.assertEqual(user.username, 'matinaa')

    def test_email(self):
        user = User.objects.get(id=30)
        self.assertEqual(user.email, 'matinaaaa@gmail.com')

