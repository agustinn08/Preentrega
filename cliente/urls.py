from django.urls import path

from . import views

app_name = "cliente"

urlpatterns = [
    path("", views.home, name="index"),
    path("busqueda/", views.busqueda),
    path("crear/", views.crear),
    path("agregar_zapatilla/", views.zapatillas_stock),
    path("ver_zapatilla/", views.view_zapatilla),
    path("crear_zapatilla/",views.crear_zapatilla),
]
