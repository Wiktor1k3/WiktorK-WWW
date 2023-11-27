from django.test import TestCase
from ..models import Person
from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory, APIClient
from rest_framework.test import force_authenticate
from django.test import TestCase
from ..views import *
from django.shortcuts import render



# initialize the APIClient app


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
    """ Testowanie bez użycia APIClient"""

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


class OsobaListTest(TestCase):
    """ Testowanie bez użycia APIClient"""

    def setUp(self) -> None:
        self.stanowisko = Stanowisko.objects.create(nazwa="Sprzątaczka")
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.zbyszek = Osoba.objects.create(
            imie='Zbyszek',nazwisko='Antczak',plec=2,stanowisko=self.stanowisko, wlasciciel=self.user)
        self.assertEqual(self.zbyszek.id,1)

    def test_get_osoby(self):
        factory = APIRequestFactory()
        request = factory.get(f'/osoba/{self.zbyszek.pk}/')
        osoba = Osoba.objects.get(pk=self.zbyszek.pk)
        serializer = OsobaSerializer(osoba)
        response = request.re
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        factory = APIRequestFactory()
        request = factory.get(f'/osoba/{self.zbyszek.id}/')
        force_authenticate(request, user=self.user)
        response = OsobaDetail.get(request, self.zbyszek.id)
        # print(response.data)  # tylko do sprawdzenia
        serializer = OsobaSerializer(self.zbyszek)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)