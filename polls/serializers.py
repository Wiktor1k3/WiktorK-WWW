from rest_framework import serializers
from .models import Person, Team, MONTHS, SHIRT_SIZES, Osoba, Stanowisko
from datetime import datetime

class PersonSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=True)
    shirt_size = serializers.ChoiceField(choices=SHIRT_SIZES, default=SHIRT_SIZES[0][0])
    data_dodania = serializers.DateField(read_only=True)
    team = serializers.PrimaryKeyRelatedField(queryset=Team.objects.all())

    def create(self, validated_data):
        return Person.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.shirt_size = validated_data.get('shirt_size', instance.shirt_size)
        instance.miesiac_dodania = validated_data.get('miesiac_dodania', instance.miesiac_dodania)
        instance.team = validated_data.get('team', instance.team)
        instance.save()
        return instance

    def validate_nazwa(self, value):

        if not value.istitle():
            raise serializers.ValidationError(
                "Nazwa osoby powinna rozpoczynać się wielką literą!",
            )
        return value

    def validate_data_dodania(self, value):

        if (value > datetime.now().date()):
            raise serializers.ValidationError(
                "Data nie może być z przyszłości!",
            )
        return value

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'


class OsobaSerializer(serializers.Serializer):
    imie = serializers.CharField(max_length=100)
    nazwisko = serializers.CharField(max_length=100)
    plec = serializers.ChoiceField(choices=Osoba.Plec.choices)
    stanowisko = serializers.PrimaryKeyRelatedField(queryset=Stanowisko.objects.all())
    data_dodania = serializers.DateField(read_only=False)

    def validate_imie(self, value):

        if not value.isalpha():
            raise serializers.ValidationError(
                "Imię osoby powinno składać się z liter!",
            )
        return value

    def validate_nazwisko(self, value):

        if not value.isalpha():
            raise serializers.ValidationError(
                "Nazwisko osoby powinno składać się z liter!",
            )
        return value

    def validate_data_dodania(self, value):

        if (value > datetime.now().date()):
            raise serializers.ValidationError(
                "Data nie może być z przyszłości!",
            )
        return value

    def create(self, validated_data):
        return Osoba.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.imie = validated_data.get('imie', instance.imie)
        instance.nazwisko = validated_data.get('nazwisko', instance.nazwisko)
        instance.plec = validated_data.get('plec', instance.plec)
        instance.stanowisko = validated_data.get('stanowisko', instance.stanowisko)
        instance.save()
        return instance


class StanowiskoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stanowisko
        fields = '__all__'
        read_only_fields = ['id']