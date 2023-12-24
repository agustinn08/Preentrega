from datetime import date

from django.shortcuts import redirect, render, get_object_or_404

from django.contrib.auth import login, logout, authenticate

# from .models import Cliente, Pais
from . import models

from datetime import datetime

#from django.contrib.auth.decorators import 

from .models import Zapatillas, Avatar
from .forms import ZapatillaForm, UserAvatarFormulario



# def home(request):
#     clientes = models.Cliente.objects.all()
#     context = {"clientes": clientes}
#     return render(request, "cliente/index.html", context)

def home(request):
    if request.user.is_authenticated:
        return redirect("cliente:index")  # Cambia a la URL deseada después del login
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

from django.shortcuts import render, redirect
from .models import Zapatillas
from .forms import ZapatillaForm

# def crear_zapatilla22(request):
#     if request.method == 'POST':
#         form = ZapatillaForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('cliente:ver_zapatilla')  
#     else:
#         form = ZapatillaForm()

#     return render(request, 'cliente/crear_zapatilla.html', {'form': form})


def view_zapatilla(request):
    zapatilla = models.Zapatillas.objects.all()
    context = {"Zapatilla" : zapatilla }
    return render(request, "cliente/ver_zapatilla.html", context)


# ...

def crear_zapatilla(request):
    if request.method == "POST":
        form = ZapatillaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("cliente:ver_zapatilla")
    else:
        form = ZapatillaForm()

    zapatillas = Zapatillas.objects.all()

    return render(request, "cliente/crear_zapatilla.html", {"form": form, "zapatillas": zapatillas})

# ...


# Vista para ver todas las zapatillas
def view_zapatilla(request):
    zapatillas = Zapatillas.objects.all()
    context = {"zapatillas": zapatillas}
    return render(request, "cliente/ver_zapatilla.html", context)

# Vista para actualizar una zapatilla

def actualizar_zapatilla(request, zapatilla_id):
    zapatilla = get_object_or_404(Zapatillas, pk=zapatilla_id)

    if request.method == "POST":
        form = ZapatillaForm(request.POST, instance=zapatilla)
        if form.is_valid():
            form.save()
            return redirect("cliente:index")  
    else:
        form = ZapatillaForm(instance=zapatilla)

    return render(request, "cliente/actualizar_zapatilla.html", {"form": form, "zapatilla": zapatilla})

# Vista para eliminar una zapatilla

def eliminar_zapatilla(request, zapatilla_id):
    zapatilla = get_object_or_404(Zapatillas, pk=zapatilla_id)
    
    if request.method == "POST":
        zapatilla.delete()
        return redirect("cliente:index")  

    return render(request, "cliente/eliminar_zapatilla.html", {"zapatilla": zapatilla})



#################### CLASE 23:  Login / Logout #########################################
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate

def login_view(request):
    if request.method == "GET":
        return render(
            request,
            "cliente/login.html",
            {"form": AuthenticationForm()}
        )
    else:
        formulario = AuthenticationForm(request, data=request.POST)
        if formulario.is_valid():
            informacion = formulario.cleaned_data
            usuario = informacion["username"]
            contraseña = informacion["password"]
            modelo = authenticate(username=usuario, password=contraseña)
            login(request, modelo)
            return redirect("cliente:index")
        else:
            return render(
                request,
                "cliente/login.html",
                {"form": formulario}
            )



def logout_view(request):
    if request.method=="GET":
        logout(request)
        return redirect("cliente:index")


from .forms import UserCreationFormulario, UserEditionFormulario
from django.contrib.auth.views import PasswordChangeView


def registro_view(request):

    if request.method == "GET":
        return render(
            request,
            "cliente/registro.html",
            {"form": UserCreationFormulario()}
        )
    else:
        formulario = UserCreationFormulario(request.POST)
        if formulario.is_valid():
            informacion = formulario.cleaned_data
            usuario = informacion["username"]
            formulario.save()

            return render(
                request,
                "cliente/inicio.html",
                {"mensaje": f"Usuario creado: {usuario}"}
            )
        else:
            return render(
                request,
                "cliente/registro.html",
                {"form": formulario}
            )
        


#############editar perfil#############


def editar_perfil_view(request):

    usuario = request.user
    avatar = Avatar.objects.filter(user=usuario).first()
    avatar_url = avatar.imagen.url if avatar is not None else ""


    if request.method == "GET":


        valores_iniciales = {
            "email": usuario.email,
            "first_name": usuario.first_name,
            "last_name": usuario.last_name
        }


        formulario = UserEditionFormulario(initial=valores_iniciales)
        return render(
            request,
            "AppCoder/editar_perfil.html",
            context={"form": formulario, "usuario": usuario, "avatar_url": avatar_url}
            )
    else:
        formulario = UserEditionFormulario(request.POST)
        if formulario.is_valid():
            informacion = formulario.cleaned_data

            usuario.email = informacion["email"]

            usuario.set_password(informacion["password1"])

            usuario.first_name = informacion["first_name"]
            usuario.last_name = informacion["last_name"]
            usuario.save()
        return redirect("AppCoder:inicio")




def crear_avatar_view(request):

    usuario = request.user

    if request.method == "GET":
        formulario = UserAvatarFormulario()
        return render(
            request,
            "AppCoder/crear_avatar.html",
            context={"form": formulario, "usuario": usuario}
        )
    else:
        formulario = UserAvatarFormulario(request.POST, request.FILES)
        if formulario.is_valid():
            informacion = formulario.cleaned_data
            modelo = Avatar(user=usuario, imagen=informacion["imagen"])
            modelo.save()
            breakpoint()
            return redirect("AppCoder:inicio")                
        

from django.shortcuts import render, get_object_or_404, redirect
from .models import Zapatillas
from .forms import ZapatillaForm

def tu_vista_de_actualizacion(request, zapatilla_id):
    # Obtén la instancia de la zapatilla que deseas actualizar
    zapatilla = get_object_or_404(Zapatillas, id=zapatilla_id)

    if request.method == 'POST':
        # Rellena el formulario con los datos del POST
        form = ZapatillaForm(request.POST, instance=zapatilla)
        if form.is_valid():
            # Guarda los cambios en la zapatilla
            form.save()
            return redirect('cliente:index', zapatilla_id=zapatilla.id)  # Reemplaza con la vista de detalle
    else:
        # Si es una solicitud GET, muestra el formulario con los datos actuales de la zapatilla
        form = ZapatillaForm(instance=zapatilla)

    return render(request, 'cliente:index', {'form': form, 'zapatilla': zapatilla})

def index(request):
    zapatilla = Zapatillas.objects.all()
    return render(request, 'core/index.html', {
        'productos': zapatilla,
        'user': request.user
        })




from django.contrib.auth.models import User
from .models import Post

