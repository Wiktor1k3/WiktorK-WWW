from django.http import HttpResponse
from rest_framework import viewsets
from .models import Person, Team
from .serializers import PersonSerializer, TeamSerializer


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer

class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer