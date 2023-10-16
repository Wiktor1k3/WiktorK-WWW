from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import Question, Team, Person

admin.site.register(Question)
admin.site.register(Team)
admin.site.register(Person)