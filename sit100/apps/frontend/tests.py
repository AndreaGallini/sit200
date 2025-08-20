from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class FeTest(TestCase):
    def setUp(self):
        # Crea un utente di test manualmente
        self.user = User.objects.create_user(
            username='testuser',  # Puoi impostare un nome utente qualunque
            email='testuser@example.com',
            password='testpsw'
        )

    def test_dashboard_success(self):
        login_successful = self.client.login(username='testuser@example.com', password='testpsw')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        
    def test_dashboard_correct_template(self):
        login_successful = self.client.login(username='testuser@example.com', password='testpsw')
        response = self.client.get(reverse('dashboard'))
        self.assertTemplateUsed(response,'frontend/homepage.html')

    def tearDown(self):
        # Pulisci il database dopo ogni test
        self.user.delete()