from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('<int:year>/<str:month>', views.home, name='home'),
    path('Eventos', views.Eventoview, name='Eventos'),
    path('addLugar', views.addLugarview, name='addLugar'),
    path('Lugars', views.Lugarlistview, name='Lugarlist'),
    path('Lugardetail/<Lugar_id>', views.Lugardetailview, name='Lugardetail'),
    path('Eventodetail/<Evento_id>', views.Eventodetailview, name="Eventodetail"),
    path('searchLugar', views.searchLugarview, name='searchLugar'),
    path('upfechaLugar/<Lugar_id>', views.upfechaLugarview, name='upfechaLugar'),
    path('deleteLugar/<Lugar_id>', views.deleteLugarview, name='deleteLugar'),
    path('Lugartext', views.Lugartext, name='Lugartext'),
    path('Lugarcsv', views.Lugarcsv, name='Lugarcsv'),
    path('Lugarpdf', views.Lugarpdf, name='Lugarpdf'),
    path('addEvento', views.addEventoview, name='addEvento'),
    path('editEvento/<Evento_id>', views.editEventoview, name='editEvento'),
    path('searchEvento', views.searchEventoview, name="searchEvento"),
    path('adminapproval', views.adminpprovalview, name="adminapproval"),
    path('EventoLugarcategory/<Lugar_id>', views.EventoLugarcategoryview, name="EventoLugarcategory"),
    
]