
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from clientes.models import Cliente
from configuracion.models import ConfiguracionERP
from productos.models import Categoria, Producto
from proveedores.models import Proveedor
from ventas.models import DetalleVenta, Pedido, Venta


def _permisos(*modelos, acciones=('add', 'change', 'delete', 'view')):
    content_type_ids = [
        ContentType.objects.get_for_model(modelo).pk
        for modelo in modelos
    ]

    return Permission.objects.filter(
        content_type_id__in=content_type_ids,
        codename__in=[
            f'{accion}_{modelo._meta.model_name}'
            for modelo in modelos
            for accion in acciones
        ]
    )


class Command(BaseCommand):
    help = 'Crea o actualiza los 3 grupos de acceso del ERP'

    def handle(self, *args, **options):
        # GERENTE: acceso completo
        gerente, creado = Group.objects.get_or_create(name='Gerente')
        permisos_gerente = _permisos(
            Cliente, Proveedor, Categoria, Producto,
            Venta, DetalleVenta, Pedido, ConfiguracionERP,
            acciones=('add', 'change', 'delete', 'view')
        )
        gerente.permissions.set(permisos_gerente)
        self.stdout.write(
            self.style.SUCCESS(
                f'Gerente: {permisos_gerente.count()} permisos asignados'
            )
        )

        # VENDEDOR: ventas y consultas
        vendedor, creado = Group.objects.get_or_create(name='Vendedor')
        permisos_vendedor = _permisos(
            Venta, DetalleVenta, Producto, Cliente,
            acciones=('add', 'view')
        )
        vendedor.permissions.set(permisos_vendedor)
        self.stdout.write(
            self.style.SUCCESS(
                f'Vendedor: {permisos_vendedor.count()} permisos asignados'
            )
        )

        # ALMACÉN: gestión de inventario
        almacen, creado = Group.objects.get_or_create(name='Almacén')
        permisos_almacen = _permisos(
            Producto, Categoria, Proveedor,
            acciones=('add', 'change', 'view')
        )
        almacen.permissions.set(permisos_almacen)
        self.stdout.write(
            self.style.SUCCESS(
                f'Almacén: {permisos_almacen.count()} permisos asignados'
            )
        )

        self.stdout.write(
            self.style.SUCCESS('Grupos y permisos configurados correctamente.')
        )
