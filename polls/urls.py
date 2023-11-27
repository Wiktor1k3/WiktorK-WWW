from django.contrib import admin
from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    # path('admin-tools/', include('admin_tools.urls'),),
    # path('', views.index, name='index'),
    # path('api/persons/', views.PersonViewSet.as_view({'get': 'list'}), name='person-list'),
    # path('api/teams/', views.TeamViewSet.as_view({'get': 'list'}), name='team-list'),
    path('osoba/', views.OsobaList.as_view()),
    path('osoba/<int:pk>/', views.OsobaDetail.as_view()),
    path('osoba/filtrowane/<str:imie>/', views.OsobaFiltered.as_view(),name='osoba-list-filtered-by-name'),
    path('stanowisko/', views.stanowisko_list),
    path('stanowisko/<int:pk>/', views.stanowisko_detail),
    path('osoba/view/<int:pk>/', views.osoba_view),
]

urlpatterns = format_suffix_patterns(urlpatterns)