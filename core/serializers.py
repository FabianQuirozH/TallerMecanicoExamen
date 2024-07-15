from rest_framework import serializers
from .models import *

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

class ProductoSerializer(serializers.ModelSerializer):
    Tipo = CategoriaSerializer(read_only = True)
    class Meta:
        model = Producto
        fields = '__all__'

