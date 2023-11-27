from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Person, Team, Osoba, Stanowisko
from django.contrib.auth.models import Permission, Group, User
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404

admin.site.register(Team)
class PersonAdmin(admin.ModelAdmin):
     list_display = ['name', 'shirt_size']
admin.site.register(Person, PersonAdmin)

class StanowiskoAdmin(admin.ModelAdmin):
    list_filter = ('nazwa',)

admin.site.register(Stanowisko, StanowiskoAdmin)

class OsobaAdmin(admin.ModelAdmin):

    @admin.display(description="Stanowisko (id)")
    def stanowisko_id(self, obj):
        return f"{obj.stanowisko.nazwa} ({obj.stanowisko.id})"

    list_display = ('__str__', 'stanowisko_id')
    list_filter = ('stanowisko', 'data_dodania')
    readonly_fields = ('data_dodania',)

admin.site.register(Osoba, OsobaAdmin)


