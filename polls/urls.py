from django.contrib import admin
from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import CustomAuthToken

from . import views

urlpatterns = [
    path('', views.index),
    path('api-auth/', include('rest_framework.urls')),
    path('api-token-auth/', CustomAuthToken.as_view()),
    path('osoba/', views.OsobaList.as_view()),
    path('osoba/detail/<int:pk>/', views.OsobaDetail.as_view()),
    path('osoba/put/<int:pk>/', views.OsobaPut.as_view()),
    path('osoba/delete/<int:pk>/', views.OsobaDelete.as_view()),
    path('osoba/filtrowane/<str:imie>/', views.OsobaFiltered.as_view(), name='osoba-list-filtered-by-name'),
    path('stanowisko/<str:stanowisko_id>/members/', views.OsobaStanowisko.as_view(), name='osoba-list-filtered-by-stanowisko'),
    path('persons/', views.person_list),
    path('person/detail/<int:pk>/', views.person_detail),
    path('person/put/<int:pk>/', views.person_update),
    path('person/delete/<int:pk>/', views.person_delete),
    path('teams/', views.teams_list),
    path('team/<int:pk>/', views.teams_detail),
    path('stanowisko/', views.stanowisko_list),
    path('stanowisko/<int:pk>/', views.stanowisko_detail),
    path('osoba/view/<int:pk>/', views.osoba_view),


]

urlpatterns = format_suffix_patterns(urlpatterns)
