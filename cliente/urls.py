from django.urls import path

from django.urls import path, include

from . import views 

from django.contrib.auth import views as auth_views

from django.contrib.auth.views import LogoutView
from django.contrib.auth.views import LoginView
from django.conf import settings
from django.conf.urls.static import static

app_name = "cliente"

from cliente.views import (
    login_view,
    registro_view,
    )

urlpatterns = [
    path("", views.home, name="index"),
    path("busqueda/", views.busqueda),
    path("cliente/", views.crear),
    path("zapatilla/",views.crear_zapatilla, name="crear_zapatilla"), 
    path("agregar_zapatilla/", views.crear_zapatilla, name="agregar_zapatilla"),
    path("ver_zapatilla/", views.view_zapatilla, name= "ver_zapatilla"),
    path("actualizar_zapatilla/<int:zapatilla_id>/", views.actualizar_zapatilla, name="actualizar_zapatilla"),
    path("eliminar_zapatilla/<int:zapatilla_id>/", views.eliminar_zapatilla, name="eliminar_zapatilla"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("registro", views.registro_view, name="registro"),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path("zapatilla/ver_zapatilla/", views.view_zapatilla, name="ver_zapatilla"),

]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)