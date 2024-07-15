from django.urls import path, include
from .views import *
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.contrib.auth import views as auth_views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('producto', ProductoViewSet)
router.register('categoria', CategoriaViewSet)

urlpatterns = [
    path('', index, name="index"),
    path('vehiculos', vehiculos, name="vehiculos"),
    path('about', about, name="about"),
    path('mecanicos', mecanicos, name="mecanicos"),
    path('contact', contact, name="contact"),
    path('services', services, name="services"),
    path('listarmecanicos/', listarmecanicos, name="listarmecanicos"),
    path('listarproductos/', listarproductos, name="listarproductos"),
    path('administrador', administrador, name="administrador"),
    path('empleadosadd', empleadosadd, name="empleadosadd"),
    path('producto_create', producto_create, name="producto_create"),
    path('producto/<int:producto_id>', producto_show, name="producto_show"),
    path('empleadosupdate/<int:id>/', empleadosupdate, name='empleadosupdate'),
    path('empleadosdelete/<int:id>/', empleadosdelete, name='empleadosdelete'),
    path('producto_edit/<int:id>/', producto_edit, name='producto_edit'),
    path('producto_delete/<int:id>/', producto_delete, name='producto_delete'),
    path('account_locked/', account_locked, name="account_locked"),
    path('registro', registro, name="registro"),
    path('carrito/', carrito, name="carrito"),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # CARRITO
    path('carrito', carrito_index, name="carrito_index"),
    path('carrito/agregar', carrito_save, name="carrito_save"),
    path('carrito/clean', carrito_clean, name="carrito_clean"),
    path('item_carrito/<int:item_carrito_id>/eliminar', item_carrito_delete, name="item_carrito_delete"),

    path('save_purchase/', save_purchase, name='save_purchase'),
    path('historial_compras/', historial_compras, name='historial_compras'),

    path('voucher/<int:compra_id>/', generar_voucher, name='generar_voucher'),



    
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="password_reset.html"), name='password_reset'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="password_reset_sent.html"), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_form.html"), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_done.html"), name='password_reset_complete'),

    path('api/', include(router.urls)),
]


