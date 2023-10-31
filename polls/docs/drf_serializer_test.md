 from polls.models import Osoba
 from polls.serializers import OsobaSerializer 
 from rest_framework.renderers import JSONRenderer
 from rest_framework.parsers import JSONParser
 from polls.models import Stanowisko
 
 stanowisko = Stanowisko.objects.get(nazwa='Nauczyciel') 
 osoba = Osoba(imie='Jan',nazwisko='Krzysiak',plec=2,stanowisko=stanowisko) 
 osoba.save() 

 serializer = OsobaSerializer(osoba)

 serializer.data 
 {'imie': 'Jan', 'nazwisko': 'Krzysiak', 'plec': 2, 'stanowisko': 3, 'data_dodania': '2023-10-31'}

 content = JSONRenderer().render(serializer.data)

 content 
 b'{"imie":"Jan","nazwisko":"Krzysiak","plec":2,"stanowisko":3,"data_dodania":"2023-10-31"}'

 import io
 stream = io.BytesIO(content)
 data = JSONParser().parse(stream)
 deserializer = OsobaSerializer(data=data)  

 deserializer.is_valid()
 True

 deserializer.save()
 <Osoba: Jan Krzysiak>

 deserializer.data
 {'imie': 'Jan', 'nazwisko': 'Krzysiak', 'plec': 2, 'stanowisko': 3, 'data_dodania': '2023-10-31'}


