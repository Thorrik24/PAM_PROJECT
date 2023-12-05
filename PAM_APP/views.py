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

#CREATE VIEWS
class CreateUsuario(CreateView):
    template_name="CRUD/crear.html"
    model = Usuario
    form_class = SingUpForm

class CreatePokemon(CreateView):
    template_name = "CRUD/crear.html"
    model = Pokemon
    fields = ["nombre","descripcion","coste","etapa","tipo_1","tipo_2"]

    def post(self,request,*args,**kwargs):
        form = request.POST
        try:
            nombre_p = request.POST["nombre"]
            descripcion_p = request.POST["descripcion"]
            coste_p = request.POST["coste"]
            etapa_p = request.POST["etapa"]
            tipo_1_p = request.POST["tipo_1"]
            tipo_2_p = request.POST["tipo_2"]
            tipo_p = "Pokemon"

            Pokemon.objects.create(nombre=nombre_p ,Descripcion=descripcion_p,
                                    Coste=coste_p, Etapa=etapa_p, tipo=tipo_p,
                                    tipo_1=tipo_1_p, tipo_2=tipo_2_p
                                    )
        except:
            #gestion de errores
            print("ERROR: No ha sido posible crear el registro.")

        return HttpResponseRedirect(reverse_lazy("pam:Cartas"))

class CreateEquipo(CreateView):
    template_name = "CRUD/crear.html"
    model = Equipo
    fields = ["nombre","descripcion","coste","tipo_equipo"]

    def post(self,request,*args,**kwargs):
        form = request.POST
        try:
            nombre_eq = request.POST["nombre"]
            descripcion_eq = request.POST["descripcion"]
            coste_eq = request.POST["coste"]
            tipo_equipo_eq = request.POST["tipo_equipo"]
            tipo_eq = "Equipo"

            Equipo.objects.create(nombre=nombre_eq, descripcion=descripcion_eq, 
                                  coste=coste_eq, tipo_equipo=tipo_equipo_eq, tipo=tipo_eq
                                  )

        except:
            print("ERROR: No ha sido posible crear el registro.")

        return HttpResponseRedirect(reverse_lazy("pam:Cartas"))

class CreateAtaque(CreateView):
    template_name = "CRUD/crear.html"
    model = Ataque
    fields = ["nombre","descripcion","coste","cara_ataque"]

    def post(self,request,*args,**kwargs):
        form = request.POST
        try:
            nombre_at = request.POST["nombre"]
            descripcion_at = request.POST["descripcion"]
            coste_at = request.POST["coste"]
            cara_ataque_at = request.POST["cara_ataque"]
            tipo_at = "Ataque"

            Ataque.objects.create(nombre=nombre_at, descripcion=descripcion_at, 
                                  coste=coste_at, cara_ataque=cara_ataque_at, tipo=tipo_at
                                  )

        except:
            print("ERROR: No ha sido posible crear el registro.")

        return HttpResponseRedirect(reverse_lazy("pam:Cartas"))

class CreateApoyo(CreateView):
    template_name = "CRUD/crear.html"
    model = Apoyo
    fields = ["nombre","descripcion","coste","tipo_apoyo"]

    def post(self,request,*args,**kwargs):
        form = request.POST
        try:
            nombre_ap = request.POST["nombre"]
            descripcion_ap = request.POST["descripcion"]
            coste_ap = request.POST["coste"]
            tipo_apoyo_ap = request.POST["tipo_apoyo"]
            tipo_ap = "Apoyo"

            Pokemon.objects.create(Nombre=nombre_ap,Descripcion=descripcion_ap,
                                    coste=coste_ap, tipo_apoyo=tipo_apoyo_ap, tipo=tipo_ap
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

class DeleteApoyo(DeleteView):
    template_name = "CRUD/eliminar.html"
    model = Apoyo
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
    
class ListadoApoyo(TemplateView):
    template_name="CRUD/listar.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object_list"] = Apoyo.objects.all()
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
    
#UPDATE VIEWS

class UpdatePokemon(UpdateView):
    template_name = 'CRUD/crear.html'
    model = Pokemon
    fields = '__all__'

class UpdateEquipo(UpdateView):
    template_name = 'CRUD/crear.html'
    model = Equipo
    fields = '__all__'

class UpdateAtaque(UpdateView):
    template_name = 'CRUD/crear.html'
    model = Ataque
    fields = '__all__'

class UpdateApoyo(UpdateView):
    template_name = 'CRUD/crear.html'
    model = Apoyo
    fields = '__all__'


#DETAIL

class DetailPokemon(DetailView):
    template_name = 'details/pokemon.html'
    queryset=Pokemon.objects.all()

class DetailAtaque(DetailView):
    template_name = 'details/ataque.html'
    queryset=Ataque.objects.all()

class DetailEquipo(DetailView):
    template_name = 'details/equipo.html'
    queryset=Equipo.objects.all()

class DetailApoyo(DetailView):
    template_name = 'details/apoyo.html'
    queryset=Apoyo.objects.all()