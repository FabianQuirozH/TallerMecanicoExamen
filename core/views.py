
from django.core.paginator import Paginator
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group  # Asegúrate de importar Group si aún no está importado
import requests
from .models import *
from .forms import *

import decimal
from django.core.exceptions import SuspiciousOperation

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

from rest_framework import viewsets
from .serializers import * 
from rest_framework.renderers import JSONRenderer



class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all().order_by('id')
    serializer_class = ProductoSerializer
    renderer_classes=[JSONRenderer]

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all().order_by('id')
    serializer_class = CategoriaSerializer
    renderer_classes=[JSONRenderer]



def index(request):
    mecanicos = Empleado.objects.all()
    aux = {'lista': mecanicos}
    return render(request, 'core/index.html', aux)

def user_in_group(user, group_name):
    return user.groups.filter(name=group_name).exists()

def group_required(group_name):
    def decorator(view_func):
        @login_required
        def wrapped_view(request, *args, **kwargs):
            if user_in_group(request.user, group_name):
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponseForbidden("No tienes permiso para acceder a esta página")
        return wrapped_view
    return decorator

def carrito(request):
    return render(request, 'core/carrito.html')

def account_locked(request):
    return render(request, 'core/account_locked.html')

def vehiculos(request):
    return render(request, 'core/vehiculos.html')

def about(request):
    return render(request, 'core/about.html')

def contact(request):
    return render(request, 'core/contact.html')

def mecanicos(request):
    mecanicos = Empleado.objects.all()
    aux = {'lista': mecanicos}
    return render(request, 'core/mecanicos.html', aux)

def services(request):
    return render(request, 'core/services.html')

def listarmecanicos(request):
    mecanicos = Empleado.objects.all()
    aux = {'lista': mecanicos}
    return render(request, 'core/listarmecanicos.html', aux)


def listarproductos(request):
    response = requests.get('http://127.0.0.1:8000/api/producto/')
    productos = response.json()
    aux = {
        'lista': productos,
    }
    return render(request, 'core/listarproductos.html', aux)

def administrador(request):
    mecanicos = Empleado.objects.all()
    productos = Producto.objects.order_by('id')
    aux = {'lista': mecanicos, 'productos': productos}
    return render(request, 'core/indexadmin.html', aux)

@login_required
def producto_show(request, producto_id):
    productos = get_object_or_404(Producto, id=producto_id)
    aux = {'productos': productos}
    return render(request, 'core/show.html', aux)

@permission_required('app_name.permission_name', raise_exception=True)
def empleadosadd(request):
    aux = {'forms': empleadoform()}
    if request.method == 'POST':
        formulario = empleadoform(data=request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "EMPLEADO GUARDADO CORRECTAMENTE")
        else:
            aux['forms'] = formulario
            messages.error(request, "NO SE PUDO GUARDAR EL EMPLEADO")
    return render(request, 'core/crud/add.html', aux)

@permission_required('app_name.permission_name', raise_exception=True)
def empleadosupdate(request, id):
    empleado = get_object_or_404(Empleado, pk=id)
    if request.method == 'POST':
        formulario = empleadoform(request.POST, request.FILES, instance=empleado)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "EMPLEADO ACTUALIZADO CORRECTAMENTE")
            return redirect('listarmecanicos')
    else:
        formulario = empleadoform(instance=empleado)
    
    aux = {'forms': formulario}
    return render(request, 'core/crud/update.html', aux)

@permission_required('app_name.permission_name', raise_exception=True)
def empleadosdelete(request, id):
    empleado = get_object_or_404(Empleado, id=id)
    empleado.delete()
    messages.success(request, "ELIMINADO CORRECTAMENTE")
    return redirect('listarmecanicos')

def registro(request):
    data = {'form': CustomUserCreationForm()}
    if request.method == 'POST':
        formulario = CustomUserCreationForm(data=request.POST)
        if formulario.is_valid():
            user = formulario.save()
            group = Group.objects.get(name='cliente')  # Asegúrate de que el grupo 'cliente' exista
            user.groups.add(group)
            user = authenticate(request=request, username=user.username, password=request.POST['password1'])
            if user is not None:
                login(request, user)
                messages.success(request, "Te has registrado correctamente")
                return redirect('login')
            else:
                messages.error(request, "Error en la autenticación. Por favor, verifica tus credenciales.")
        else:
            data['form'] = formulario
            messages.error(request, "Formulario no válido. Por favor, corrige los errores.")
    return render(request, 'registration/register.html', data)
@permission_required('app_name.permission_name', raise_exception=True)
def producto_create(request):
    aux = {
        'forms' : productoform()
    }
    if request.method == 'POST':
        formulario = productoform(data=request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "PRODUCTO GUARDADO CORRECTAMENTE")
        else:
            aux['forms'] = formulario
            messages.error(request, "NO SE PUDO GUARDAR EL PRODUCTO")
    return render(request, 'core/crudproductos/addproducto.html',aux)

@permission_required('app_name.permission_name', raise_exception=True)
def producto_edit(request, id):
    producto_instance = get_object_or_404(Producto, pk=id)  # Use a different variable name
    if request.method == 'POST':
        formulario = productoform(request.POST, request.FILES, instance=producto_instance)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "PRODUCTO ACTUALIZADO CORRECTAMENTE")
            return redirect('listarproductos')  # Redirigir a la lista de productos después de actualizar
    else:
        formulario = productoform(instance=producto_instance)
    
    aux = {'forms': formulario}
    return render(request, 'core/crudproductos/updateproducto.html', aux)

@permission_required('app_name.permission_name', raise_exception=True)
def producto_delete(request, id):
    if request.method == "POST":
        producto = get_object_or_404(Producto, id=id)
        producto.delete()
        messages.success(request, "Producto eliminado correctamente.")
    return redirect('listarproductos')

""" 
    Carrito productos
"""
@login_required
def carrito_index(request):
    categorias = Categoria.objects.all()
    usuario_logeado = request.user

   
    carrito, created = Carrito.objects.get_or_create(usuario=usuario_logeado, defaults={'total': 0})

    productos = carrito.items.all()

  
    nuevo_precio_carrito = sum(item.producto.precio for item in productos)

    carrito.total = nuevo_precio_carrito
    carrito.save()

    
    total_carrito = format(carrito.total, '.2f').replace(",", ".")

    return render(request, 'carrito/carrito.html', {
        'categorias': categorias,
        'usuario': usuario_logeado,
        'items_carrito': productos,
        'total_carrito': total_carrito,
    })



@login_required
def carrito_save(request):
    if request.method == 'POST':
        try:
            producto = Producto.objects.get(id=request.POST['producto_id'])
            usuario_logeado = request.user

            try:
                respuesta = requests.get('https://mindicador.cl/api/dolar')
                respuesta.raise_for_status()  # Asegura que la solicitud fue exitosa (status code 200)
                valor_usd = decimal.Decimal(respuesta.json()['serie'][0]['valor'])  # Convertir a Decimal

                carrito, created = Carrito.objects.get_or_create(usuario=usuario_logeado)
                item_carrito = Carrito_item(carrito=carrito, producto=producto)
                item_carrito.save()

                carrito.total += producto.precio
                carrito.total = round(carrito.total / valor_usd, 2)
                carrito.save()

                messages.success(request, f"El producto {producto.titulo} fue agregado al carrito")
            except requests.RequestException as e:
                messages.error(request, f"Error al obtener el valor del dólar: {str(e)}")
            except (KeyError, IndexError) as e:
                messages.error(request, f"Error en el formato de los datos recibidos: {str(e)}")
        except Producto.DoesNotExist:
            messages.error(request, "El producto no existe.")
        
        return redirect("administrador")
    else:
        return redirect("administrador")



@login_required
def carrito_clean(request):
    usuario_logeado = request.user
    carrito = Carrito.objects.get(usuario=usuario_logeado)
    carrito.items.all().delete()
    carrito.total = 0
    carrito.save()
    return redirect('carrito_index')

@login_required
def item_carrito_delete(request, item_carrito_id):
    item_carrito = get_object_or_404(Carrito_item, id=item_carrito_id)
    carrito = item_carrito.carrito

    carrito.total -= item_carrito.producto.precio
    item_carrito.delete()
    carrito.save()
    return redirect("carrito_index")




#ESTE ES EL CODIGO SIN FALLOS

@csrf_exempt
def save_purchase(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            total = decimal.Decimal(data.get('total'))
            items = data.get('items', [])

            compra = Compra.objects.create(usuario=request.user, total=total)

            for item in items:
                producto_id = item.get('producto_id')
                cantidad = item.get('cantidad', 1)
                precio_unitario = item.get('precio_unitario')
                
                producto = Producto.objects.get(id=producto_id)
                CompraItem.objects.create(compra=compra, producto=producto, cantidad=cantidad, precio=precio_unitario)

            # Vaciar el carrito después de la compra
            carrito = Carrito.objects.get(usuario=request.user)
            carrito.items.all().delete()
            carrito.total = 0
            carrito.save()

            messages.success(request, 'Compra realizada correctamente.')

            return JsonResponse({'status': 'success'})

        except Producto.DoesNotExist:
            return JsonResponse({'status': 'failed', 'error': "Uno o más productos no existen."})

        except Exception as e:
            return JsonResponse({'status': 'failed', 'error': str(e)})

    return JsonResponse({'status': 'failed', 'error': 'Invalid request method.'})

def historial_compras(request):
    compras = Compra.objects.filter(usuario=request.user).order_by('-fecha')

    # Paginación
    paginator = Paginator(compras, 3)  # 3 compras por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    compras_dict = {}
    for compra in page_obj:
        items = CompraItem.objects.filter(compra=compra)
        compras_dict[compra.id] = {
            'compra': compra,
            'items': items
        }

    return render(request, 'core/historial_compras.html', {
        'compras_dict': compras_dict,
        'page_obj': page_obj
    })

def generar_voucher(request, compra_id):
    compra = get_object_or_404(Compra, id=compra_id, usuario=request.user)
    items = CompraItem.objects.filter(compra=compra)

    # Crear el PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="voucher_compra_{compra.id}.pdf"'

    c = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    c.drawString(1 * inch, height - 1 * inch, f"Voucher de Compra #{compra.id}")
    c.drawString(1 * inch, height - 1.5 * inch, f"Fecha: {compra.fecha.strftime('%Y-%m-%d %H:%M:%S')}")
    c.drawString(1 * inch, height - 2 * inch, f"Usuario: {compra.usuario.username}")
    c.drawString(1 * inch, height - 2.5 * inch, f"Total: ${compra.total}")

    y_position = height - 3.5 * inch
    for item in items:
        c.drawString(1 * inch, y_position, f"{item.producto.titulo} - Cantidad: {item.cantidad} - Precio: ${item.precio}")
        y_position -= 0.5 * inch

    c.showPage()
    c.save()

    return response