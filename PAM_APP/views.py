from typing import Any
from django.shortcuts import render
from PAM_APP.models import *
from django.views.generic import *
from django.urls import reverse_lazy
from .forms import *
#from .forms import *
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect

#AUTORIZACIÓN
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import Q
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.postgres.search import TrigramWordSimilarity
from django.utils import timezone
from django.template import RequestContext
from django.db import IntegrityError
from django.shortcuts import render

#EXCEPCIÓN
class CosteSuperado(Exception):
    ...
    pass

class Index(TemplateView):
    template_name="index.html"

class ListadoCartas(ListView):
    template_name = "CRUD/listar.html"
    model = Carta

#DETAIL

class DetailPokemon(DetailView):
    template_name = 'CRUD/detail.html'
    queryset=Pokemon.objects.all()

#UPDATE

class UpdatePokemon(UpdateView):
    template_name = 'CRUD/crear.html'
    model = Pokemon
    fields = '__all__'
#CREATE VIEWS
class CreateUsuario(CreateView):
    template_name="CRUD/crear.html"
    model = Usuario
    form_class = SingUpForm

class CreatePokemon(CreateView):
    template_name = "CRUD/crear.html"
    model = Pokemon
    fields = ["Nombre","Descripcion","Coste","Etapa","tipo_1","tipo_2"]

    def post(self,request,*args,**kwargs):
        form = request.POST
        try:
            nombre = request.POST["Nombre"]
            descripcion = request.POST["Descripcion"]
            coste = request.POST["Coste"]
            etapa = request.POST["Etapa"]
            tipo_1 = request.POST["tipo_1"]
            tipo_2 = request.POST["tipo_2"]
            tipo = "Pokemon"

            Pokemon.objects.create(Nombre=nombre,Descripcion=descripcion,
                                    Coste=coste, Etapa=etapa, Tipo=tipo,
                                    tipo_1=tipo_1, tipo_2=tipo_2
                                    )
        except:
            print("ERROR: No ha sido posible crear el registro.")

        return HttpResponseRedirect(reverse_lazy("pam:Cartas"))

class CreateEquipo(CreateView):
    template_name = "CRUD/crear.html"
    model = Equipo
    fields = ["Nombre","Descripcion","Coste","TipoEquipo"]

    def post(self,request,*args,**kwargs):
        form = request.POST
        try:
            nombre = request.POST["Nombre"]
            descripcion = request.POST["Descripcion"]
            coste = request.POST["Coste"]
            Tipo_Equipo = request.POST["TipoEquipo"]
            tipo = "Equipo"

            Equipo.objects.create(Nombre=nombre, Descripcion=descripcion, 
                                  Coste=coste, TipoEquipo=Tipo_Equipo, Tipo=tipo
                                  )

        except:
            print("ERROR: No ha sido posible crear el registro.")

        return HttpResponseRedirect(reverse_lazy("pam:Cartas"))

class CreateAtaque(CreateView):
    template_name = "CRUD/crear.html"
    model = Ataque
    fields = ["Nombre","Descripcion","Coste","CaraAtaque"]

    def post(self,request,*args,**kwargs):
        form = request.POST
        try:
            nombre = request.POST["Nombre"]
            descripcion = request.POST["Descripcion"]
            coste = request.POST["Coste"]
            cara_ataque = request.POST["CaraAtaque"]
            tipo = "Ataque"

            Ataque.objects.create(Nombre=nombre, Descripcion=descripcion, 
                                  Coste=coste, CaraAtaque=cara_ataque, Tipo=tipo
                                  )

        except:
            print("ERROR: No ha sido posible crear el registro.")

        return HttpResponseRedirect(reverse_lazy("pam:Cartas"))

class CreateHechizo(CreateView):
    template_name = "CRUD/crear.html"
    model = Hechizo
    fields = ["Nombre","Descripcion","Coste","TipoHechizo"]

    def post(self,request,*args,**kwargs):
        form = request.POST
        try:
            nombre = request.POST["Nombre"]
            descripcion = request.POST["Descripcion"]
            coste = request.POST["Coste"]
            rango_carta = request.POST["TipoHechizo"]
            tipo = "Hechizo"

            Pokemon.objects.create(Nombre=nombre,Descripcion=descripcion,
                                    Coste=coste, TipoHechizo=rango_carta, Tipo=tipo
                                    )
        except:
            print("ERROR: No ha sido posible crear el registro.")

        return HttpResponseRedirect(reverse_lazy("pam:Cartas"))

class CreateBarajas(CreateView):
    model = Baraja
    fields=["Nombre","Descripcion"]
    template_name = 'Barajas/crear-baraja.html'
    success_url = reverse_lazy('pam:Index')
    def form_valid(self, form):
        try:
            self.object = form.save(commit=False)
            self.object.Usuario = self.request.user
            self.object.save()
            return HttpResponseRedirect(reverse_lazy('pam:LBaraja'))
        except IntegrityError as e:
            return render(self.request,'CRUD/crear-baraja.html', {"message":"ERROR: La baraja ya existe!!!","form":form})

class AñadirCartas(CreateView):
    model = Registro
    template_name = "Barajas/añadir-cartas.html"
    fields = ['Carta','Equipo','Ataque']

    def form_valid(self,form):
        try:
            self.object = form.save(commit=False)
            self.object.Baraja = Baraja.objects.get(id=self.request.GET.get("q"))

            try:
                Bara = Baraja.objects.get(id=self.request.GET.get("q"))
                coste_actual = Baraja.objects.get(id=self.request.GET.get("q")).Coste #OBTENER COSTE ACTUAL
                
                
                nuevo_coste = coste_actual 

                #SUMAR COSTES
                if self.object.Ataque:
                    nuevo_coste += self.object.Ataque.Coste
                if self.object.Equipo:
                    nuevo_coste += self.object.Equipo.Coste

                nuevo_coste +=  self.object.Carta.Coste

                if nuevo_coste <= 20:
                    Bara.Coste = nuevo_coste
                    Bara.save()
                else:
                    raise CosteSuperado

            except CosteSuperado as e:

                return render(self.request,'Barajas/añadir-cartas.html', {"message":"ERROR: El coste de la baraja supera al permitido","form":form})

            try:
                if self.object.Baraja.Usuario.id == self.request.user.id:
                    self.object.save()
                    return HttpResponseRedirect(reverse_lazy('pam:LBaraja'))
                else:
                    raise PermissionError 


            except PermissionError:
                return render(self.request,'Barajas/añadir-cartas.html', {"message":"ERROR: No tienes permisos para editar esa baraja","form":form})
        except IntegrityError as e:
            return render(self.request,'Barajas/añadir-cartas.html', {"message":"ERROR: Ese Pokemon ya se encuentra en la baraja","form":form})
        
 


#DELETE VIEWS
class DeletePokemon(DeleteView):
    template_name = "CRUD/eliminar.html"
    model = Pokemon
    success_url = reverse_lazy("pam:Cartas")

class DeleteAtaque(DeleteView):
    template_name = "CRUD/eliminar.html"
    model = Ataque
    success_url = reverse_lazy("pam:Cartas")

class DeleteEquipo(DeleteView):
    template_name = "CRUD/eliminar.html"
    model = Equipo
    success_url = reverse_lazy("pam:Cartas")

class DeleteHechizo(DeleteView):
    template_name = "CRUD/eliminar.html"
    model = Hechizo
    success_url = reverse_lazy("pam:Cartas")

#LIST VIEWS
class ListadoPokemon(TemplateView):
    template_name="CRUD/listar.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object_list"] = Pokemon.objects.all()
        return context
    
class ListadoAtaque(TemplateView):
    template_name="CRUD/listar.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object_list"] = Ataque.objects.all()
        return context

class ListadoEquipo(TemplateView):
    template_name="CRUD/listar.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object_list"] = Equipo.objects.all()
        return context
    
class ListadoHechizo(TemplateView):
    template_name="CRUD/listar.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object_list"] = Hechizo.objects.all()
        return context

class ListadoBaraja(TemplateView):
    template_name="Barajas/listar.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object_list"] = Baraja.objects.filter(Usuario=self.request.user)
        return context

class DetailBaraja(DetailView):
    model = Baraja
    template_name = "Barajas/DetailBaraja.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["registros"] = Registro.objects.filter(Baraja=Baraja.objects.get(id=self.request.META["PATH_INFO"].split("/")[-1]))
        return context
    
        
        
    