from django.contrib.auth.models import AnonymousUser
from rest_framework.authentication import BasicAuthentication, TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Osoba, Stanowisko, Person, Team
from .serializers import OsobaSerializer, StanowiskoSerializer, PersonSerializer, TeamSerializer
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.http import Http404, HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from polls.permissions import IsOwnerOrReadOnly
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

class OsobaList(APIView):
    def get(self, request, format=None):
        osoby = []
        if not isinstance(self.request.user, AnonymousUser):
            osoby = Osoba.objects.filter(wlasciciel=self.request.user)
        serializer = OsobaSerializer(osoby, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = OsobaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(wlasciciel=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OsobaFiltered(APIView):
    def get(self, request, imie, format=None):
        osoby = Osoba.objects.filter(imie__icontains=imie)
        serializer = OsobaSerializer(osoby, many=True)
        return Response(serializer.data)

class OsobaStanowisko(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, stanowisko_id, format=None):
        osoby = Osoba.objects.filter(stanowisko_id=stanowisko_id)
        if not osoby:
            return Response({"message": "Brak osób przypisanych do danego stanowiska."},status=status.HTTP_404_NOT_FOUND)
        serializer = OsobaSerializer(osoby, many=True)
        return Response(serializer.data)

class OsobaDetail(APIView):
    permission_classes = [IsOwnerOrReadOnly]
    def get_object(self, pk):
        try:
            return Osoba.objects.get(pk=pk)
        except Osoba.DoesNotExist:
            raise Http404
    def get(self, request, pk, format=None):
        osoba = self.get_object(pk)
        self.check_object_permissions(request, osoba)
        serializer = OsobaSerializer(osoba)
        return Response(serializer.data)

class OsobaPut(APIView):
    permission_classes = [IsOwnerOrReadOnly]

    def get_object(self, pk):
        try:
            return Osoba.objects.get(pk=pk)
        except Osoba.DoesNotExist:
            raise Http404
    def get(self, request, pk, format=None):
        osoba = self.get_object(pk)
        self.check_object_permissions(request, osoba)
        serializer = OsobaSerializer(osoba)
        return Response(serializer.data)
    def put(self, request, pk, format=None):
        osoba = self.get_object(pk)
        self.check_object_permissions(request, osoba)

        serializer = OsobaSerializer(osoba, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OsobaDelete(APIView):
    permission_classes = [IsOwnerOrReadOnly]
    def get_object(self, pk):
        try:
            return Osoba.objects.get(pk=pk)
        except Osoba.DoesNotExist:
            raise Http404
    def get(self, request, pk, format=None):
        osoba = self.get_object(pk)
        self.check_object_permissions(request, osoba)
        serializer = OsobaSerializer(osoba)
        return Response(serializer.data)
    def delete(self, request, pk, format=None):
        osoba = self.get_object(pk)
        self.check_object_permissions(request, osoba)

        osoba.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def person_list(request):
    """
    Lista wszystkich obiektów modelu Person.
    """
    if request.method == 'GET':
        persons = Person.objects.all()
        serializer = PersonSerializer(persons, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def person_detail(request, pk):

    """
    :param request: obiekt DRF Request
    :param pk: id obiektu Person
    :return: Response (with status and/or object/s data)
    """
    try:
        person = Person.objects.get(pk=pk)
    except Person.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    """
    Zwraca pojedynczy obiekt typu Person.
    """
    if request.method == 'GET':
        person = Person.objects.get(pk=pk)
        serializer = PersonSerializer(person)
        return Response(serializer.data)


@api_view(['PUT'])
def person_update(request, pk):
    try:
        person = Person.objects.get(pk=pk)
    except Person.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = PersonSerializer(person, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def person_delete(request, pk):
    try:
        person = Person.objects.get(pk=pk)
    except Person.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'DELETE':
        person.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET','POST'])
def teams_list(request):
    if request.method == 'GET':
        teams = Team.objects.all()
        serializer = TeamSerializer(teams, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = TeamSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def teams_detail(request, pk):

    try:
        team = Team.objects.get(pk=pk)
    except Team.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    """
    Zwraca pojedynczy obiekt typu Osoba.
    """
    if request.method == 'GET':
        team = Team.objects.get(pk=pk)
        serializer = TeamSerializer(team)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = TeamSerializer(team, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        team.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET','POST'])
def stanowisko_list(request):
    if request.method == 'GET':
        stanowiska = Stanowisko.objects.all()
        serializer = StanowiskoSerializer(stanowiska, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = StanowiskoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def stanowisko_detail(request, pk):

    """
    :param request: obiekt DRF Request
    :param pk: id obiektu Stanowisko
    :return: Response (with status and/or object/s data)
    """
    try:
        stanowisko = Stanowisko.objects.get(pk=pk)
    except Stanowisko.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    """
    Zwraca pojedynczy obiekt typu Osoba.
    """
    if request.method == 'GET':
        stanowisko = Stanowisko.objects.get(pk=pk)
        serializer = StanowiskoSerializer(stanowisko)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = StanowiskoSerializer(stanowisko, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        stanowisko.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

