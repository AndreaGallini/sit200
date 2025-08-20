from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class LegalTest(TestCase):
    def setUp(self):
        # Crea un utente di test manualmente
        self.user = User.objects.create_user(
            username='testuser',  # Puoi impostare un nome utente qualunque
            email='testuser@example.com',
            password='testpsw'
        )

    def test_cookies_success(self):
        login_successful = self.client.login(username='testuser@example.com', password='testpsw')
        response = self.client.get(reverse('cookies'))
        self.assertEqual(response.status_code, 200)
        
    def test_cookies_correct_template(self):
        login_successful = self.client.login(username='testuser@example.com', password='testpsw')
        response = self.client.get(reverse('cookies'))
        self.assertTemplateUsed(response,'legal/cookies.html')

    def test_privacy_success(self):
        login_successful = self.client.login(username='testuser@example.com', password='testpsw')
        response = self.client.get(reverse('privacy'))
        self.assertEqual(response.status_code, 200)
        
    def test_privacy_correct_template(self):
        login_successful = self.client.login(username='testuser@example.com', password='testpsw')
        response = self.client.get(reverse('privacy'))
        self.assertTemplateUsed(response,'legal/privacy.html')

    def test_terms_conditions_success(self):
        login_successful = self.client.login(username='testuser@example.com', password='testpsw')
        response = self.client.get(reverse('terms_conditions'))
        self.assertEqual(response.status_code, 200)
        
    def test_terms_conditions_correct_template(self):
        login_successful = self.client.login(username='testuser@example.com', password='testpsw')
        response = self.client.get(reverse('terms_conditions'))
        self.assertTemplateUsed(response,'legal/terms_conditions.html')
    def tearDown(self):
        # Pulisci il database dopo ogni test
        self.user.delete()