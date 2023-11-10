from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    # path('admin-tools/', include('admin_tools.urls'),),
    # path('', views.index, name='index'),
    # path('api/persons/', views.PersonViewSet.as_view({'get': 'list'}), name='person-list'),
    # path('api/teams/', views.TeamViewSet.as_view({'get': 'list'}), name='team-list'),
    path('osoba/', views.osoba_list),
    path('osoba/<int:pk>/', views.osoba_detail),
    path('osoba/filtrowane/', views.osoba_list_filtered, name='osoba-list-filtered'),
    path('stanowisko/', views.stanowisko_list),
    path('stanowisko/<int:pk>/', views.stanowisko_detail),


]
