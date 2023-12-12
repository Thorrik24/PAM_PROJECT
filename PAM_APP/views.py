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
class search(ListView):
    model = Pokemon
    template_name="Barajas/search.html"
    def get_queryset(self):
        query = self.request.GET.get("q")
        object_list=Pokemon.objects.filter(Q(nombre__icontains=query))
        return object_list

class ListadoCartas(TemplateView):
    template_name = "CRUD/listar.html"
    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["pokemons"] = Pokemon.objects.all()
        context["ataques"] = Ataque.objects.all()
        context["apoyos"] = Apoyo.objects.all()
        context["equipos"] = Equipo.objects.all()
        return context
    

#CREATE VIEWS
class CreateUsuario(CreateView):
    template_name="registration/login.html"
    model = Usuario
    form_class = SingUpForm

class CreatePokemon(UserPassesTestMixin,CreateView):
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
    def test_func(self): #COMPROBAR SI POSEE PERMISOS (ERROR 403: FORBIDDEN)
            try:
                return self.request.user.is_superuser
            except:
                return False

class CreateEquipo(UserPassesTestMixin,CreateView):
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

    def test_func(self): #COMPROBAR SI POSEE PERMISOS (ERROR 403: FORBIDDEN)
            try:
                return self.request.user.is_superuser
            except:
                return False
class CreateAtaque(UserPassesTestMixin,CreateView):
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
    def test_func(self): #COMPROBAR SI POSEE PERMISOS (ERROR 403: FORBIDDEN)
            try:
                return self.request.user.is_superuser
            except:
                return False
class CreateApoyo(UserPassesTestMixin,CreateView):
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
    def test_func(self): #COMPROBAR SI POSEE PERMISOS (ERROR 403: FORBIDDEN)
            try:
                return self.request.user.is_superuser
            except:
                return False

#VISTAS RELACIONADAS CON LAS BARAJAS Y USUARIO [CREARLAS, ELIMINARLAS, MODIFICARLAS]
class CreateBarajas(UserPassesTestMixin,CreateView):
    model = Baraja
    fields=["nombre","descripcion"]
    template_name = 'Barajas/crear-baraja.html'
    success_url = reverse_lazy('pam:Index')
    def form_valid(self, form):
        try:
            self.object = form.save(commit=False)
            self.object.usuario = self.request.user
            self.object.save()
            return HttpResponseRedirect(reverse_lazy('pam:LBaraja'))
        except IntegrityError as e:
            return render(self.request,'Barajas/crear-baraja.html', {"message":"ERROR: La baraja ya existe!!!","form":form})
            
    def test_func(self): #COMPROBAR SI POSEE PERMISOS (ERROR 403: FORBIDDEN)
        try:
            return self.request.user.is_authenticated
        except:
            return False
class AñadirCartas(UserPassesTestMixin,CreateView):
    model = Registro
    template_name = "Barajas/añadir-cartas.html"
    fields = ['carta','equipo','ataque']

    def form_valid(self,form):
        try:
            self.object = form.save(commit=False)
            self.object.baraja = Baraja.objects.get(id=self.request.GET.get("q"))
            try:
                Bara = Baraja.objects.get(id=self.request.GET.get("q"))
                coste_actual = Baraja.objects.get(id=self.request.GET.get("q")).coste #OBTENER COSTE ACTUAL

                
                nuevo_coste = coste_actual 

                #SUMAR COSTES
                if self.object.ataque:
                    nuevo_coste += self.object.ataque.coste
                if self.object.equipo:
                    nuevo_coste += self.object.equipo.coste

                nuevo_coste +=  self.object.carta.coste

                if nuevo_coste <= 20:
                    Bara.coste = nuevo_coste
                    
                else:
                    raise CosteSuperado

            except CosteSuperado as e:

                return render(self.request,'Barajas/añadir-cartas.html', {"message":"ERROR: El coste de la baraja supera al permitido","form":form})

            try:
                if self.object.baraja.usuario.id == self.request.user.id:
                    self.object.save()
                    Bara.save()
                    return HttpResponseRedirect(reverse_lazy('pam:LBaraja'))
                else:
                    raise PermissionError 


            except PermissionError:
                return render(self.request,'Barajas/añadir-cartas.html', {"message":"ERROR: No tienes permisos para editar esa baraja","form":form})
        except IntegrityError as e:
            return render(self.request,'Barajas/añadir-cartas.html', {"message":"ERROR: Ese Pokemon ya se encuentra en la baraja","form":form})
        
    def test_func(self): #COMPROBAR SI POSEE PERMISOS (ERROR 403: FORBIDDEN)
        try:
            return Baraja.objects.get(id=self.request.GET.get("q")).usuario == self.request.user
        except:
            return False
class DetailBaraja(UserPassesTestMixin,DetailView):
    model = Baraja
    template_name = "Barajas/DetailBaraja.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["registros"] = Registro.objects.filter(baraja=Baraja.objects.get(id=self.request.META["PATH_INFO"].split("/")[-1]))
        return context

    def test_func(self): #COMPROBAR SI POSEE PERMISOS (ERROR 403: FORBIDDEN)
        try:
            return Baraja.objects.get(id=self.request.META["PATH_INFO"].split("/")[-1]).usuario == self.request.user
        except:
            return False
class DeleteCarta(UserPassesTestMixin,TemplateView):
    template_name = "Barajas/ListarCartas.html"
    model = Registro
    success_url = reverse_lazy("pam:LBaraja")

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["object_list"] = Registro.objects.filter(baraja=Baraja.objects.get(id=self.request.GET.get("q")))
        return context

    def post(self, request):
        if self.request.POST.get("e"):
            carta = Registro.objects.get(id=int(self.request.POST.get("e")))
            coste = carta.carta.coste
            if carta.equipo:
                coste += carta.equipo.coste
            if carta.ataque:
                coste += carta.ataque.coste
            baraja = Baraja.objects.get(id=self.request.META["QUERY_STRING"].split("=")[-1])
            baraja.coste -= coste
            baraja.save()
            carta.delete()

        return HttpResponseRedirect(reverse_lazy('pam:LBaraja'))
        
   
    def test_func(self): #COMPROBAR SI POSEE PERMISOS (ERROR 403: FORBIDDEN)
        try:
            return Baraja.objects.get(id=self.request.GET.get("q")).usuario == self.request.user
        except:
            return False

class ListadoBaraja(UserPassesTestMixin,TemplateView):
    template_name="Barajas/listar.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object_list"] = Baraja.objects.filter(usuario=self.request.user)
        return context
    def test_func(self): #COMPROBAR SI POSEE PERMISOS (ERROR 403: FORBIDDEN)
        try:
            return self.request.user.is_authenticated
        except:
            return False
class DeleteBaraja(UserPassesTestMixin,DeleteView):
    template_name = "CRUD/eliminar.html"
    model = Baraja
    success_url = reverse_lazy("pam:LBaraja")
    def test_func(self): #COMPROBAR SI POSEE PERMISOS (ERROR 403: FORBIDDEN)
        try:
            return Baraja.objects.get(id=self.request.META["PATH_INFO"].split("/")[-1]).usuario == self.request.user
        except:
            return False
#DELETE VIEWS
class DeletePokemon(UserPassesTestMixin,DeleteView):
    template_name = "CRUD/eliminar.html"
    model = Pokemon
    success_url = reverse_lazy("pam:Cartas")
    def test_func(self): #COMPROBAR SI POSEE PERMISOS (ERROR 403: FORBIDDEN)
            try:
                return self.request.user.is_superuser
            except:
                return False
class DeleteAtaque(UserPassesTestMixin,DeleteView):
    template_name = "CRUD/eliminar.html"
    model = Ataque
    success_url = reverse_lazy("pam:Cartas")
    def test_func(self): #COMPROBAR SI POSEE PERMISOS (ERROR 403: FORBIDDEN)
            try:
                return self.request.user.is_superuser
            except:
                return False
class DeleteEquipo(UserPassesTestMixin,DeleteView):
    template_name = "CRUD/eliminar.html"
    model = Equipo
    success_url = reverse_lazy("pam:Cartas")
    def test_func(self): #COMPROBAR SI POSEE PERMISOS (ERROR 403: FORBIDDEN)
            try:
                return self.request.user.is_superuser
            except:
                return False
class DeleteApoyo(UserPassesTestMixin,DeleteView):
    template_name = "CRUD/eliminar.html"
    model = Apoyo
    success_url = reverse_lazy("pam:Cartas")
    def test_func(self): #COMPROBAR SI POSEE PERMISOS (ERROR 403: FORBIDDEN)
            try:
                return self.request.user.is_superuser
            except:
                return False
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




#UPDATE VIEWS

class UpdatePokemon(UserPassesTestMixin,UpdateView):
    template_name = 'CRUD/crear.html'
    model = Pokemon
    fields = '__all__'
    def test_func(self): #COMPROBAR SI POSEE PERMISOS (ERROR 403: FORBIDDEN)
            try:
                return self.request.user.is_superuser
            except:
                return False
class UpdateEquipo(UserPassesTestMixin,UpdateView):
    template_name = 'CRUD/crear.html'
    model = Equipo
    fields = '__all__'
    def test_func(self): #COMPROBAR SI POSEE PERMISOS (ERROR 403: FORBIDDEN)
            try:
                return self.request.user.is_superuser
            except:
                return False
class UpdateAtaque(UserPassesTestMixin,UpdateView):
    template_name = 'CRUD/crear.html'
    model = Ataque
    fields = '__all__'
    def test_func(self): #COMPROBAR SI POSEE PERMISOS (ERROR 403: FORBIDDEN)
            try:
                return self.request.user.is_superuser
            except:
                return False
class UpdateApoyo(UserPassesTestMixin,UpdateView):
    template_name = 'CRUD/crear.html'
    model = Apoyo
    fields = '__all__'
    def test_func(self): #COMPROBAR SI POSEE PERMISOS (ERROR 403: FORBIDDEN)
            try:
                return self.request.user.is_superuser
            except:
                return False

#DETAIL

class DetailPokemon(DetailView):
    template_name = 'Detail/detailcarta.html'
    queryset=Pokemon.objects.all()

class DetailAtaque(DetailView):
    template_name = 'Detail/detailataque.html'
    queryset=Ataque.objects.all()

class DetailEquipo(DetailView):
    template_name = 'Detail/detailequipo.html'
    queryset=Equipo.objects.all()

class DetailApoyo(DetailView):
    template_name = 'Detail/detailapoyo.html'
    queryset=Apoyo.objects.all()
