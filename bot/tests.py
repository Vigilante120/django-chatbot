from django.contrib.auth import get_user_model, authenticate
from django.test import TestCase, Client
from bot.models import Chat
from django.urls import reverse
import json

User = get_user_model()


class ModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        cls.chat = Chat.objects.create(
            user=cls.user, message="Test message", response="Test response"
        )

    def test_user_creation(self):
        self.assertEqual(self.user.username, "testuser")
        self.assertTrue(self.user.is_active)
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)
        self.assertTrue(isinstance(self.user, User))

    def test_password_hashing(self):
        self.assertNotEqual(self.user.password, "testpassword")
        self.assertTrue(self.user.check_password("testpassword"))

    def test_change_password(self):
       # Change the user's password and ensure it's hashed
        new_password = 'newtestpassword'
        self.user.set_password(new_password)
        self.user.save()

        # Ensure the new password is hashed
        self.assertNotEqual(self.user.password, new_password)
        self.assertTrue(self.user.check_password(new_password))

    def test_authenticate(self):
       # Test with correct password
        self.assertIsNotNone(authenticate(username="testuser", password="testpassword"))

        # Test with incorrect password
        self.assertIsNone(authenticate(username="testuser", password="wrongpassword"))


    def test_chat_model(self):
        self.assertEqual(self.chat.user, self.user)
        self.assertEqual(self.chat.message, "Test message")
        self.assertEqual(self.chat.response, "Test response")

    def test_chat_string_representation(self):
        self.assertEqual(str(self.chat), f"{self.chat.user.username}: {self.chat.message}")

class ViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', password='testpassword'
        )

    def test_bot_view_get(self):
        # Ensure the bot view returns a status code of 200 for a GET request
        response = self.client.get(reverse("bot"))
        self.assertEqual(response.status_code, 200)

    def test_bot_view_post(self):
        # Ensure the bot view returns a JsonResponse for a POST request
        self.client.force_login(self.user)
        response = self.client.post(reverse("bot"), {'message': 'Test message'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['message'], 'Test message')
        
    def test_login_view(self):
        # Ensure the login view redirects to the bot view on successful login
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'testpassword'})
        self.assertRedirects(response, reverse('bot'))

        # Ensure the login view shows an error message on unsuccessful login
        response = self.client.post(reverse('login'), {'username': 'invaliduser', 'password': 'invalidpassword'})
        self.assertContains(response, 'Invalid username or password')

    def test_register_view(self):
        # Ensure the register view redirects to the bot view on successful registration
        response = self.client.post(reverse('register'), {'username': 'newuser', 'email': 'newuser@example.com', 'password1': 'newpassword', 'password2': 'newpassword'})
        self.assertRedirects(response, reverse('bot'))

        # Ensure the register view shows an error message on unsuccessful registration
        response = self.client.post(reverse('register'), {'username': 'testuser', 'email': 'testuser@example.com', 'password1': 'testpassword', 'password2': 'testpassword'})
        self.assertContains(response, 'Error creating account')

    def test_logout_view(self):
        # Ensure the logout view redirects to the login view
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse('login'))
       


