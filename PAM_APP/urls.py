from django.contrib import admin
from django.urls import path
from PAM_APP.views import *
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', Index.as_view(), name="Index"),
    #LISTADO
    path('cartas/', ListadoCartas.as_view(), name="Cartas"),
    path('cartas/pokemon', ListadoPokemon.as_view(), name="LPokemon"),
    path('cartas/ataque', ListadoAtaque.as_view(), name="LAtaque"),
    path('cartas/equipo', ListadoEquipo.as_view(), name="LEquipo"),
    path('cartas/apoyo', ListadoApoyo.as_view(), name="LApoyo"),

    #BARAJAS
    path('baraja/', ListadoBaraja.as_view(), name="LBaraja"),
    #REGISTROS (CARTA, EQUIPAMIENTO)
    path('baraja/añadir', AñadirCartas.as_view(), name="AñaBara"),
    #DETALLADAS
    path('baraja/detail/<int:pk>', DetailBaraja.as_view(), name="DetailBaraja"),
    
    #CREAR
    path('register', CreateUsuario.as_view(), name="CUser"),
    path('create/pokemon', CreatePokemon.as_view(), name="CPoke"),
    path('create/ataque', CreateAtaque.as_view(), name="CAta"),
    path('create/equipo', CreateEquipo.as_view(), name="CEqui"),
    path('create/apoyo', CreateApoyo.as_view(), name="CApoyo"),
    path('create/baraja', CreateBarajas.as_view(), name="CBara"),
    
    #BORRAR
    path('delete/pokemon/<int:pk>', DeletePokemon.as_view(), name="DPoke"),
    path('delete/ataque/<int:pk>', DeleteAtaque.as_view(), name="DAta"),
    path('delete/equipo/<int:pk>', DeleteEquipo.as_view(), name="DEqui"),
    path('delete/apoyo/<int:pk>', DeleteApoyo.as_view(), name="DApoyo"),
    #DETAIL

    path('detail/pokemon/<int:pk>', DetailPokemon.as_view(), name="DtPoke"),
    path('detail/ataque/<int:pk>', DetailAtaque.as_view(), name="DtAta"),
    path('detail/equipo/<int:pk>', DetailEquipo.as_view(), name="DtEqui"),
    path('detail/apoyo/<int:pk>', DetailApoyo.as_view(), name="DtApoyo"),
    #UPDATE
    path('update/pokemon/<int:pk>', UpdatePokemon.as_view(), name="UpPoke"),
    path('update/equipo/<int:pk>', UpdateEquipo.as_view(), name="UpEqui"),
    path('update/ataque/<int:pk>', UpdateAtaque.as_view(), name="UpAta"),
    path('update/apoyo/<int:pk>', UpdateApoyo.as_view(), name="UpApoyo"),
]
]