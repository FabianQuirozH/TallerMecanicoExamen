from django.contrib import admin
from .models import *
from admin_confirm import AdminConfirmMixin

class TipoEmpleadoAdmin(AdminConfirmMixin, admin.ModelAdmin):
    confirm_change = True
    confirmation_fields = ['descripcion']
# Register your models here.

class EmpleadoAdmin(AdminConfirmMixin, admin.ModelAdmin):
    confirm_change = True
    confirmation_fields = ['nombre', 'apellido','edad','imagen','Tipo']

class CategoriasAdmin(AdminConfirmMixin, admin.ModelAdmin):
    confirm_change = True
    confirmation_fields = ['descripcion']

class ProductosAdmin(AdminConfirmMixin, admin.ModelAdmin):
    confirm_change = True
    confirmation_fields = ['titulo', 'imagen','descripcion','precio','categoria']

# Register your models here.
admin.site.register(tipoempleado,TipoEmpleadoAdmin)
admin.site.register(Empleado,EmpleadoAdmin)
admin.site.register(Categoria,CategoriasAdmin)
admin.site.register(Producto,ProductosAdmin)