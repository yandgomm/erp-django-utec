"""Serializers de la app productos — W10."""
from rest_framework import serializers

from .models import Categoria, Producto


class CategoriaSerializer(serializers.ModelSerializer):
    """Serializer de Categoria — campos completos."""

    class Meta:
        model            = Categoria
        fields           = ['id', 'nombre', 'descripcion']
        read_only_fields = ['id']


class ProductoSerializer(serializers.ModelSerializer):
    """Serializer de Producto con nombre de categoría y proveedor."""

    categoria_nombre = serializers.CharField(
        source='categoria.nombre',
        read_only=True
    )
    proveedor_nombre = serializers.CharField(
        source='proveedor.nombre',
        read_only=True,
        allow_null=True
    )

    class Meta:
        model  = Producto
        fields = [
            'id', 'nombre', 'precio', 'stock',
            'categoria', 'categoria_nombre',
            'proveedor', 'proveedor_nombre',
            'activo', 'creado',
        ]
        read_only_fields = ['id', 'creado', 'categoria_nombre', 'proveedor_nombre']