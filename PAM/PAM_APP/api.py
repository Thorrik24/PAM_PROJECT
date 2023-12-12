from rest_framework import routers, serializers, viewsets
from .models import *
# Serializers define the API representation.
router = routers.DefaultRouter()

class PokemonSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Pokemon
        fields = ["nombre","descripcion","coste","etapa","tipo_1","tipo_2"]

# ViewSets define the view behavior.
class PokemonViewSet(viewsets.ModelViewSet):
    queryset = Pokemon.objects.all()
    serializer_class = PokemonSerializer


# Routers provide an easy way of automatically determining the URL conf.

router.register(r'api/pokemons', PokemonViewSet)


class AtaqueSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Ataque
        fields = ["nombre","descripcion","coste","CaraAtaque"]

# ViewSets define the view behavior.
class AtaqueViewSet(viewsets.ModelViewSet):
    queryset = Ataque.objects.all()
    serializer_class = AtaqueSerializer


# Routers provide an easy way of automatically determining the URL conf.
router.register(r'api/ataques', AtaqueViewSet)


class ApoyoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Apoyo
        fields = ["nombre","descripcion","coste","tipo_apoyo"]

# ViewSets define the view behavior.
class ApoyoViewSet(viewsets.ModelViewSet):
    queryset = Apoyo.objects.all()
    serializer_class = ApoyoSerializer


# Routers provide an easy way of automatically determining the URL conf.
router.register(r'api/apoyos', ApoyoViewSet)


class EquipoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Equipo
        fields = ["nombre","descripcion","coste","TipoEquipo"]

# ViewSets define the view behavior.
class EquipoViewSet(viewsets.ModelViewSet):
    queryset = Equipo.objects.all()
    serializer_class = EquipoSerializer


# Routers provide an easy way of automatically determining the URL conf.
router.register(r'api/equipos', EquipoViewSet)