from django.http import HttpResponse
from rest_framework import viewsets, status
from .models import Person, Team,Osoba,Stanowisko
from .serializers import PersonSerializer, TeamSerializer, OsobaSerializer, StanowiskoSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

# class PersonViewSet(viewsets.ModelViewSet):
#     queryset = Person.objects.all()
#     serializer_class = PersonSerializer
#
# class TeamViewSet(viewsets.ModelViewSet):
#     queryset = Team.objects.all()
#     serializer_class = TeamSerializer

@api_view(['GET','POST'])
def osoba_list(request):
    if request.method == 'GET':
        osoby = Osoba.objects.all()
        serializer = OsobaSerializer(osoby, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = OsobaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# POST - Dodawanie osoby w chrome przez konsole:
# // Pobierz token CSRF z ciasteczka
# const csrfToken = document.cookie.match(/csrftoken=([^ ;]*)/)[1];
#
# fetch('http://127.0.0.1:8000/osoba/', {
#   method: 'POST',
#   headers: {
#     'Content-Type': 'application/json',
#     'X-CSRFToken': csrfToken,
#   },
#   body: JSON.stringify({
#     "imie": "Nowa",
#     "nazwisko": "Osoba",
#     "plec": 1,
#     "stanowisko": 1,  // Zastąp 1 odpowiednim ID stanowiska
#     "data_dodania": "2023-01-01",  // Zastąp odpowiednią datą
#   }),
# })
# .then(response => response.json())
# .then(data => console.log(data))
# .catch(error => console.error('Error:', error));

@api_view(['GET'])
def osoba_list_filtered(request):
    imie_param = request.query_params.get('imie', '')

    osoby = Osoba.objects.filter(imie__icontains=imie_param)

    serializer = OsobaSerializer(osoby, many=True)
    return Response(serializer.data)

@api_view(['GET', 'PUT', 'DELETE'])
def osoba_detail(request, pk):

    """
    :param request: obiekt DRF Request
    :param pk: id obiektu Osoba
    :return: Response (with status and/or object/s data)
    """
    try:
        osoba = Osoba.objects.get(pk=pk)
    except Osoba.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    """
    Zwraca pojedynczy obiekt typu Osoba.
    """
    if request.method == 'GET':
        osoba = Osoba.objects.get(pk=pk)
        serializer = OsobaSerializer(osoba)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = OsobaSerializer(osoba, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        osoba.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# PUT - edytowanie obiektów Osoba:
# Content:
# {
#   "imie": "NoweImie",
#   "nazwisko": "NoweNazwisko",
#   "plec": 1,
#   "stanowisko": 1,
#   "data_dodania": "2023-01-01"
# }


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

# POST - Dodawanie stanowiska w chrome przez konsole:
# // Pobierz token CSRF z ciasteczka
# const csrfToken = document.cookie.match(/csrftoken=([^ ;]*)/)[1];
#
# fetch('http://127.0.0.1:8000/stanowisko/', {
#   method: 'POST',
#   headers: {
#     'Content-Type': 'application/json',
#     'X-CSRFToken': csrfToken,
#   },
#   body: JSON.stringify({
#     "nazwa": "Mechanik",
#     "opis": "naprawia samochody",
#   }),
# })
# .then(response => response.json())
# .then(data => console.log(data))
# .catch(error => console.error('Error:', error));

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

# PUT - Edytowanie obiektów stanowisko_detail:
# Content:
# {
#   "stanowisko": "Kasjer",
#   "opis": "Sprzedaje",
# }
