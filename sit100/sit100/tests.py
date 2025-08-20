from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import RequestFactory
from unittest.mock import patch
import json


class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpass')



def test_project_map_view(self):
    url = reverse('project_map')
    response = self.client.get(url)
    self.assertEqual(response.status_code, 200)
    self.assertIn('time', response.context)
    self.assertIn('lat', response.context)
    self.assertIn('lon', response.context)
    # Check session data
    self.assertIn('project', self.client.session)
    project = self.client.session['project']
    self.assertIn('project_code', project)


def test_inclination_view_get(self):
    self.client.login(username='testuser', password='testpass')
    session = self.client.session
    session['project'] = {'polygons': [{'name': 'polygon1'}]}
    session.save()
    url = reverse('inclination')
    response = self.client.get(url)
    self.assertEqual(response.status_code, 200)
    self.assertIn('polygons', response.context)

def test_inclination_view_post(self):
    self.client.login(username='testuser', password='testpass')
    session = self.client.session
    session['project'] = {'polygons': [{'name': 'polygon1'}]}
    session.save()
    selected_angles = [{'polygonName': 'polygon1', 'angle': 45}]
    response = self.client.post(
        reverse('inclination'),
        {'selectedAngles': json.dumps(selected_angles)}
    )
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.json(), {'message': 'Angoli salvati con successo.'})
    session = self.client.session
    polygons = session['project']['polygons']
    self.assertEqual(polygons[0]['angle'], 45)



def test_get_pvgis_data_view(self):
    with patch('requests.get') as mocked_get:
        mocked_get.return_value.status_code = 200
        mocked_get.return_value.json.return_value = {'outputs': {'some_data': 'value'}}
        response = self.client.post(
            reverse('get_pvgis_data'),
            data={'lat': '50', 'lon': '14', 'peakpower': '1', 'loss': '14'}
        )
        expected_url = 'https://re.jrc.ec.europa.eu/api/v5_2/PVcalc?lat=50&lon=14&peakpower=1&loss=14&outputformat=json'
        mocked_get.assert_called_with(expected_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'outputs': {'some_data': 'value'}})


def test_clear_session_view(self):
    session = self.client.session
    session['project'] = {'some': 'data'}
    session.save()
    response = self.client.get(reverse('clear_session'))
    self.assertNotIn('project', self.client.session)
    self.assertEqual(response.status_code, 302)  # Redirect status code
    self.assertRedirects(response, '/fe')



def test_clear_coordinates_view(self):
    session = self.client.session
    session['project'] = {'lat': '50', 'lon': '14', 'altitude': '100'}
    session.save()
    response = self.client.post(reverse('clear_coordinates'))
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.json(), {'message': 'Coordinates cleared from project'})
    project = self.client.session['project']
    self.assertNotIn('lat', project)
    self.assertNotIn('lon', project)
    self.assertNotIn('altitude', project)