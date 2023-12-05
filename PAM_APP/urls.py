from django.contrib import admin
from django.urls import path
from PAM_APP.views import *
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', Index.as_view(), name="Index"),
    #LISTADO
    path('Cartas/', ListadoCartas.as_view(), name="Cartas"),
    path('Cartas/pokemon', ListadoPokemon.as_view(), name="LPokemon"),
    path('Cartas/ataque', ListadoAtaque.as_view(), name="LAtaque"),
    path('Cartas/equipo', ListadoEquipo.as_view(), name="LEquipo"),
    path('Cartas/hechizo', ListadoHechizo.as_view(), name="LHechizo"),

    #BARAJAS
    path('Baraja/', ListadoBaraja.as_view(), name="LBaraja"),
    #REGISTROS (CARTA, EQUIPAMIENTO)
    path('baraja/añadir', AñadirCartas.as_view(), name="AñaBara"),
    #DETALLADAS
    path('baraja/detail/<int:pk>', DetailBaraja.as_view(), name="DetailBaraja"),
    
    #CREAR
    path('register', CreateUsuario.as_view(), name="CUser"),
    path('create/pokemon', CreatePokemon.as_view(), name="CPoke"),
    path('create/ataque', CreateAtaque.as_view(), name="CAta"),
    path('create/equipo', CreateEquipo.as_view(), name="CEqui"),
    path('create/hechizo', CreateHechizo.as_view(), name="CHechi"),
    path('create/baraja', CreateBarajas.as_view(), name="CBara"),
    
    #BORRAR
    path('delete/pokemon/<int:pk>', DeletePokemon.as_view(), name="DPoke"),
    path('delete/ataque/<int:pk>', DeleteAtaque.as_view(), name="DAta"),
    path('delete/equipo/<int:pk>', DeleteEquipo.as_view(), name="DEqui"),
    path('delete/hechizo/<int:pk>', DeleteHechizo.as_view(), name="DHechi"),
    #DETAIL

    path('detail/pokemon/<int:pk>', DetailPokemon.as_view(), name="DtPoke"),

    #UPDATE
    path('update/pokemon/<int:pk>', UpdatePokemon.as_view(), name="UpPoke"),
]