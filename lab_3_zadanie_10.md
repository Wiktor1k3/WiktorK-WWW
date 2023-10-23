>>> from polls.models import Osoba
>>> all_people = Osoba.objects.all()
>>> print(all_people)
<QuerySet [<Osoba: Asia Krzysiak>, <Osoba: Marianna Nowacka>, <Osoba: Jan Nowak>]>

>>> osoba_id_3 = Osoba.objects.get(id=3)
>>> print(osoba_id_3)
Asia Krzysiak

>>> osoby_na_M = Osoba.objects.filter(imie__istartswith='M') 
>>> print(osoby_na_M) 
<QuerySet [<Osoba: Marianna Nowacka>]>

>>> unikalne_stanowiska = Osoba.objects.values_list('stanowisko',flat=True).distinct()
>>> print(unikalne_stanowiska)
<QuerySet [3, 2, 1]>

>>> stanowiska_posortowane = sorted(unikalne_stanowiska, reverse=True)
>>> print(stanowiska_posortowane)
[3, 2, 1]
