from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class tipoempleado(models.Model):
    descripcion = models.CharField(max_length=100)

    def __str__(self):
        return self.descripcion

class Empleado(models.Model):
    nombre = models.CharField(max_length=30)
    apellido = models.CharField(max_length=30)
    edad = models.IntegerField(default=0)
    imagen = models.ImageField( upload_to= "mecanicoimg", null=True)
    tipo = models.ForeignKey(tipoempleado,  on_delete=models.CASCADE)
    
    def __str__(self):

        return self.nombre
    

    
class Categoria(models.Model):
    descripcion = models.CharField(max_length=200, null=False)

    def __str__(self) -> str:
        return f"Id: {self.pk} | Descripcion: {self.descripcion}"
    


class Producto(models.Model):
    titulo = models.CharField(max_length=50, null=False)
    imagen = models.FileField(upload_to="producto", null=True)
    descripcion = models.CharField(max_length=200, null=False)
    precio = models.DecimalField(null=False, max_digits=10, decimal_places=2)
 
    categoria = models.ForeignKey(Categoria,on_delete=models.CASCADE, related_name="productos")

    def __str__(self) -> str:
        return f"Id: {self.pk} | Titulo: {self.titulo} | Imagen: {self.imagen} | Descripcion: {self.descripcion} | Precio: {self.precio} || Categoria_id: {self.categoria.id} "


"""class Carrito(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="carrito")
    total = models.DecimalField(null=False, max_digits=10, decimal_places=2)

    def __str__(self) -> str:
        return f"Id: {self.pk} | Usuario_id: {self.usuario.id} | Usuario: {self.usuario.username} | Total: {self.total}"""
class Carrito(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="carrito")
    total = models.IntegerField(default=0)

    def __str__(self):
        return f"Id: {self.pk} | Usuario_id: {self.usuario.id} | Usuario: {self.usuario.username} | Total: {self.total}"



class Carrito_item(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE) 
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, related_name="items")

    def __str__(self) -> str:
        return f"Id: {self.pk} | Producto: {self.producto.titulo} | Carrito_id: {self.carrito.id}"



class Compra(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Compra #{self.pk} - Usuario: {self.usuario.username} - Total: {self.total}"

class CompraItem(models.Model):
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Item de compra #{self.compra.pk} - Producto: {self.producto.titulo} - Cantidad: {self.cantidad} - Precio: {self.precio}"