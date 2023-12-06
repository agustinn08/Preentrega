from django import forms

from . import models


class ClienteForm(forms.ModelForm):
    class Meta:
        model = models.Cliente
        fields = ["nombre", "apellido", "nacimiento", "pais_origen"]

class ZapatillaForm(forms.ModelForm):
    class Meta:
        model = models.Zapatillas
        fields = "__all__"

