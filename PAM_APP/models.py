from django.utils.translation import gettext_lazy as _
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.core.validators import MaxValueValidator,MinValueValidator
from django.forms import ModelChoiceField
from itertools import chain
from django.db.models.query_utils import Q

class Usuario(AbstractUser):
    Alias = models.CharField(max_length=35,null=False,blank=False)
    Nombre = models.CharField(max_length=60,null=False,blank=False)
    Apellido = models.CharField(max_length=160)
    #Avatar = models.ImageField(blank=True, null=True)

    

    def __str__(self):
        return self.Alias

class Carta(models.Model):
    Nombre =  models.CharField(max_length=150)
    Descripcion = models.CharField(max_length=150)
    #TIPOS DE CARTA QUE PUEDEN EXISTIR
    class Variaciones(models.TextChoices):
        POKEMON = "Pokemon", _("Pokemon")
        ATAQUE = "Ataque", _("Ataque")
        EQUIPO = "Equipo", _("Equipo")
        HECHIZO = "Hechizo", _("Hechizo")
    Coste = models.PositiveIntegerField(null=False,blank=True)
    Tipo = models.CharField(max_length=10, choices=Variaciones.choices, default="Pokemon")
    #Imagen = models.ImageField(upload_to="media/", height_field=None, width_field=None, max_length=None)
    def __str__(self):
        return f"{self.Nombre}"

class Pokemon(Carta):
    type=[
        ("A", "Acero"),
        ("W", "Agua"),
        ("B", "Bicho"),
        ("D", "Dragon"),
        ("E", "Eléctrico"),
        ("G", "Fantasma"),
        ("F", "Fuego"),
        ("H", "Hada"),
        ("I", "Hielo"),
        ("L", "Lucha"),
        ("N", "Normal"),
        ("P", "Planta"),
        ("Ps", "Psíquico"),
        ("R", "Roca"),
        ("S", "Siniestro"),
        ("T", "Tierra"),
        ("V", "Veneno"),
        ("Fl", "Volador")
    ]
    etapas = [('INI','inicial'),('INT','intermedia'),('AVA','avanzado')]
    
    Etapa = models.CharField(max_length=50, choices=etapas)
    tipo_1 = models.CharField(max_length=50, choices=type)
    tipo_2 = models.CharField(max_length=50, choices=type, blank=True,null=True)

    def get_absolute_url(self):
         return reverse('pam:DtPoke', kwargs={'pk': self.pk})

    def __str__(self):
        return f"{self.Nombre}"

class Equipo(Carta):

    type=[
        ("O", "Objeto de batalla"),
        ("S", "Piedras"),
        ("B", "Bayas")
    ]
    TipoEquipo=models.CharField(max_length=15, choices=type)

    def __str__(self):
        return f"{self.Nombre}"

class Ataque(Carta):
    
    type=[
        ("A", "Ataque A"),
        ("B", "Ataque B")
    ]
    CaraAtaque=models.CharField(max_length=3, choices=type )
    def __str__(self):
        return f"{self.Nombre}"

class Hechizo(Carta):
    type=[
        ("MT","MT"),
        ("MO","Mo"),
        ("Ev","Evento")
    ]

    TipoHechizo=models.CharField(max_length=6, choices=type)

    def __str__(self):
        return f"{self.Nombre}"

class Baraja(models.Model):
    Usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    Nombre = models.CharField(max_length=100, null=False, blank=False)
    Descripcion = models.CharField(max_length=100,null=False, blank=False)
    cartas = models.ManyToManyField(Pokemon, through='Registro')
    Coste = models.PositiveIntegerField(validators=[MaxValueValidator(20),],null=False,blank=True,default=0)

    class Meta:
        unique_together = (('Usuario','Nombre'),)

    def __str__(self):
        return f"Baraja: {self.Nombre} | {self.Coste}"

class Registro(models.Model):
    Baraja = models.ForeignKey(Baraja,on_delete=models.CASCADE)
    Carta = models.ForeignKey(Pokemon,on_delete=models.CASCADE)
    Equipo = models.ForeignKey(Equipo,on_delete=models.CASCADE,null=True,blank=True)
    Ataque = models.ForeignKey(Ataque,on_delete=models.CASCADE,null=True,blank=True)
    class Meta:
        unique_together = (('Baraja','Carta'),)
        
    def __str__(self):
        return f"{self.Baraja}-{self.Carta}-{self.Equipo}"
