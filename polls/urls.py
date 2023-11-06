from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/persons/', views.PersonViewSet.as_view({'get': 'list'}), name='person-list'),
    path('api/teams/', views.TeamViewSet.as_view({'get': 'list'}), name='team-list'),
]