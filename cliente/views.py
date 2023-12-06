from datetime import date

from django.shortcuts import redirect, render

# from .models import Cliente, Pais
from . import models


def home(request):
    clientes = models.Cliente.objects.all()
    context = {"clientes": clientes}
    return render(request, "cliente/index.html", context)



def busqueda(request):
    # búsqueda por nombre que contenga "dana"
    cliente_nombre = models.Cliente.objects.filter(nombre__contains="dana")

    # nacimientos mayores a 2000
    cliente_nacimiento = models.Cliente.objects.filter(nacimiento__gt=date(2000, 1, 1))

    # país de origen vacío (null - None)
    cliente_pais = models.Cliente.objects.filter(pais_origen=None)

    context = {
        "cliente_nombre": cliente_nombre,
        "cliente_nacimiento": cliente_nacimiento,
        "cliente_pais": cliente_pais,
    }
    return render(request, "cliente/busqueda.html", context)


from . import forms


def crear(request):
    if request.method == "POST":
        form = forms.ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("cliente:index")
    else:
        form = forms.ClienteForm()
    return render(request, "cliente/crear.html", {"form": form})


def zapatillas_stock(request):
    c1 = models.Zapatillas(nombre="air force one", modelo="air force", marca="nike", talle= 41)
    c1.save()
    return redirect("cliente:index")

def view_zapatilla(request):
    zapatilla = models.Zapatillas.objects.all()
    context = {"Zapatilla" : zapatilla }
    return render(request, "cliente/ver_zapatilla.html", context)


def crear_zapatilla(request):
    if request.method == "POST":
        form = forms.ZapatillaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("cliente:index")
    else:
        form = forms.ZapatillaForm()
    return render(request, "cliente/crear_zapatilla.html", {"form": form})
