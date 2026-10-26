# ventas/models.py
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models

from clientes.models import Cliente
from productos.models import Producto


# -- Venta ------------------------------------------------------------------

class Venta(models.Model):
    """Encabezado de una venta interna.

    El total no se almacena en la BD (D-04); se calcula
    sumando los subtotales de cada DetalleVenta asociado.
    """

    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.PROTECT,      # D-03: no borrar cliente con ventas
        related_name='ventas',
        verbose_name='Cliente'
    )
    fecha = models.DateTimeField(
        auto_now_add=True, verbose_name='Fecha'
    )

    class Meta:
        verbose_name        = 'Venta'
        verbose_name_plural = 'Ventas'
        ordering            = ['-fecha']

    def __str__(self) -> str:
        return f"Venta #{self.pk} - {self.cliente} ({self.fecha:%d/%m/%Y})"

    @property
    def total(self) -> Decimal:
        """Total de la venta: suma de subtotales de cada linea (D-04)."""
        return sum(
            (d.subtotal for d in self.detalles.all()),
            Decimal('0.00')
        )


# -- DetalleVenta -----------------------------------------------------------

class DetalleVenta(models.Model):
    """Linea de producto dentro de una venta.

    precio_unitario se almacena (D-06) porque el precio del producto
    puede cambiar despues de la venta; se necesita el historico exacto.
    """

    venta = models.ForeignKey(
        Venta,
        on_delete=models.CASCADE,
        related_name='detalles',
        verbose_name='Venta'
    )
    producto = models.ForeignKey(
        Producto,
        on_delete=models.PROTECT,      # D-05: no borrar producto con ventas
        related_name='detalles_venta',
        verbose_name='Producto'
    )
    cantidad = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='Cantidad'
    )
    precio_unitario = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='Precio unitario',
        help_text='Precio al momento de la venta (D-06). '
                  'Si se deja vacio, se toma del producto.'
    )

    class Meta:
        verbose_name        = 'Detalle de venta'
        verbose_name_plural = 'Detalles de venta'

    def __str__(self) -> str:
        return f"{self.producto.nombre} x {self.cantidad}"

    @property
    def subtotal(self) -> Decimal:
        """Subtotal de la linea: cantidad x precio_unitario."""
        return self.precio_unitario * self.cantidad

    def clean(self) -> None:
        """Validacion de negocio para linea de detalle.

        Raises:
            ValidationError: si cantidad < 1.
        """
        if self.cantidad is not None and self.cantidad < 1:
            raise ValidationError(
                {'cantidad': 'La cantidad debe ser al menos 1.'}
            )

    def save(self, *args, **kwargs):
        """Copia el precio del producto si no se indico uno."""
        if self.precio_unitario is None and self.producto_id:
            self.precio_unitario = self.producto.precio
        super().save(*args, **kwargs)


# -- Pedido -----------------------------------------------------------------

class Pedido(models.Model):
    """Orden de compra del canal e-commerce (se implementa en la Espiral 5)."""

    ESTADO_CHOICES = [
        ('pendiente',  'Pendiente de pago'),
        ('pagado',     'Pago confirmado'),
        ('enviado',    'En camino'),
        ('entregado',  'Entregado'),
        ('cancelado',  'Cancelado'),
    ]

    numero_pedido = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='Numero de pedido',
        help_text='Formato sugerido: PED-YYYY-NNNN'
    )
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.PROTECT,
        related_name='pedidos',
        verbose_name='Cliente'
    )
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='pendiente',
        verbose_name='Estado'
    )
    fecha_pedido = models.DateTimeField(
        auto_now_add=True, verbose_name='Fecha del pedido'
    )
    fecha_entrega = models.DateField(
        null=True, blank=True, verbose_name='Fecha de entrega'
    )
    total_pagado = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name='Total pagado'
    )

    class Meta:
        verbose_name        = 'Pedido'
        verbose_name_plural = 'Pedidos'
        ordering            = ['-fecha_pedido']

    def __str__(self) -> str:
        return f"{self.numero_pedido} - {self.cliente} [{self.get_estado_display()}]"

    def clean(self) -> None:
        """Valida que la fecha de entrega no sea anterior al pedido.

        Raises:
            ValidationError: si fecha_entrega < fecha_pedido.date().
        """
        if (self.fecha_entrega and self.fecha_pedido and
                self.fecha_entrega < self.fecha_pedido.date()):
            raise ValidationError({
                'fecha_entrega': (
                    'La fecha de entrega no puede ser anterior '
                    'a la fecha del pedido.'
                )
            })