import graphene
from graphene_django import DjangoObjectType
from polls.models import Person, Team

class PersonType(DjangoObjectType):
    class Meta:
        model = Person
        fields = ("id", "name", "shirt_size", "data_dodania")

class TeamType(DjangoObjectType):
    class Meta:
        model = Team
        fields = ("id", "name", "country")


class Query(graphene.ObjectType):
    all_teams = graphene.List(TeamType)
    person_by_id = graphene.Field(PersonType, id=graphene.Int(required=True))
    people_by_name = graphene.List(PersonType, name=graphene.String())
    people_by_data_dodania = graphene.List(PersonType, date=graphene.String(required=True))
    people_by_date = graphene.List(PersonType)


    def resolve_all_teams(root, info):
        return Team.objects.all()

    def resolve_person_by_id(root, info, id):
        try:
            return Person.objects.get(pk=id)
        except Person.DoesNotExist:
            raise Exception('Invalid person Id')

    def resolve_person_by_name(root, info, name):
        try:
            return Person.objects.filter(name__icontains=name)
        except Person.DoesNotExist:
            raise Exception('Bad')

    def resolve_person_by_data_dodania(root,info,date):
        try:
            return Person.objects.filter(data_dodania=date)
        except ValueError:
            raise Exception('Bad')

    def resolve_people_sorted_by_date(root, info):
        try:
            return Person.objects.all().order_by('data_dodania')
        except Person.DoesNotExist:
            raise Exception('Bad')




schema = graphene.Schema(query=Query)
