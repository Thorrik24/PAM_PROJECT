from django.contrib.auth.forms import UserCreationForm
from .models import *
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from django import forms
from django.forms import inlineformset_factory
from itertools import product
from django.forms.formsets import BaseFormSet
class SingUpForm(UserCreationForm):
    class Meta:
      model = Usuario
      fields = ('username', 'password1', 'password2','email','Alias','Nombre','Apellido')


# forms.py

# class BarajaForm(forms.Form):
#     CHOICES = [(x,f'{x} No items') for x in Pokemon.objects.all()]
#     CHOICES += [(f"{x}-{y}",f"{x} {y}") for x,y in product(list(Pokemon.objects.all()), list(Equipo.objects.all()))]
#     Nombre = forms.CharField( max_length=100, required=True)
#     Descripcion = forms.CharField( max_length=100, required=True)
#     objeto = forms.MultipleChoiceField(choices=CHOICES,label='Carta',widget=forms.CheckboxSelectMultiple)

class BarajaForm(forms.Form):
  nombre = forms.CharField( max_length=100, required=True)
  descripcion = forms.CharField(max_length=100, required=True)

# class AñadirCartas(forms.Form):
