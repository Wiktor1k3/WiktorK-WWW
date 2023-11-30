from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory, APIClient
from rest_framework.test import force_authenticate
from django.test import TestCase
from ..views import *

class PersonModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Person.objects.create(name='Jan', shirt_size='L')

    def test_first_name_label(self):
        person = Person.objects.get(id=1)
        field_label = person._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_first_name_max_length(self):
        person = Person.objects.get(id=1)
        max_length = person._meta.get_field('name').max_length
        self.assertEqual(max_length, 60)

client = APIClient()

class AddPersonAndTeamTest(TestCase):

    def setUp(self):
        self.team1 = Team.objects.create(name='Loosers', country='PL')
        self.team2 = Team.objects.create(name='Snakes', country='EN')
        self.zbyszek = Person.objects.create(
            name='Zbyszek', shirt_size='L', data_dodania=1, team=self.team1)
        self.andrzej = Person.objects.create(
            name='Andrzej', shirt_size='L', data_dodania=1, team=self.team2)


    def test_person_id(self):
        self.assertEqual(self.zbyszek.id, 1)
        self.assertEqual(self.andrzej.id, 2)

    def test_team_id(self):
        self.assertEqual(self.team1.id,1)
        self.assertEqual(self.team2.id, 2)
        self.assertEqual(self.zbyszek.team.id, self.team1.id)
        self.assertEqual(self.andrzej.team.id, self.team2.id)

class OsobaListTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user', password='password')

    def test_osoba_list_authenticated(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('osoba-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_osoba_list_unauthenticated(self):
        self.client.logout()
        url = reverse('osoba-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class StanowiskoAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.get(user=self.user)
        self.client = APIClient()


    def test_authentication_with_token_and_create_stanowisko(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        data = {'nazwa': 'Murarz', 'opis': 'Opis stanowiska'}
        url = reverse('stanowisko-list')
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['nazwa'], 'Murarz')


class TeamsAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_authentication_with_force_authenticate_and_create_stanowisko(self):
        factory = APIRequestFactory()
        url = reverse('teams-list')
        request = factory.post(url, {'name': 'Locky', 'country': 'PL'}, format='json')
        force_authenticate(request, user=self.user)
        response = teams_list(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(response.data['name'], 'Locky')
