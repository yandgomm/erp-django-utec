# Entidades y Atributos — ERP Django

## Entidad 1 — Categoria

| Atributo | Tipo Django | Restricción | Justificación |
|---|---|---|---|
| id | BigAutoField | PK, auto | Clave primaria generada |
| nombre | CharField(100) | unique, not null | Sin categorías duplicadas |
| descripcion | TextField | blank=True | Opcional |

## Entidad 2 — Proveedor

| Atributo | Tipo Django | Restricción | Justificación |
|---|---|---|---|
| id | BigAutoField | PK, auto | Clave primaria generada |
| nombre | CharField(150) | not null | Nombre comercial |
| contacto | CharField(100) | blank=True | Persona de contacto |
| correo | EmailField | unique, not null | Identificador único |
| telefono | CharField(20) | blank=True | Formato libre |
| activo | BooleanField | default=True | Soft-delete |
| creado | DateTimeField | auto_now_add | Trazabilidad |

## Entidad 3 — Cliente

| Atributo | Tipo Django | Restricción | Justificación |
|---|---|---|---|
| id | BigAutoField | PK, auto | Clave primaria generada |
| nombre | CharField(150) | not null | Nombre o razón social |
| correo | EmailField | unique, not null | Contacto principal |
| telefono | CharField(20) | blank=True | Opcional |
| activo | BooleanField | default=True | Soft-delete |
| creado | DateTimeField | auto_now_add | Trazabilidad |

## Entidad 4 — Producto

| Atributo | Tipo Django | Restricción | Justificación |
|---|---|---|---|
| id | BigAutoField | PK, auto | |
| nombre | CharField(200) | not null | Nombre del artículo |
| precio | DecimalField(10,2) | MinValueValidator(0) | Precio mayor o igual a 0 |
| stock | IntegerField | default=0, MinValue(0) | No puede ser negativo |
| categoria | ForeignKey(Categoria) | PROTECT | Decisión D-01 |
| proveedor | ForeignKey(Proveedor) | SET_NULL, null=True | Decisión D-02 |
| activo | BooleanField | default=True | Soft-delete |
| creado | DateTimeField | auto_now_add | Trazabilidad |

## Entidad 5 — Venta

| Atributo | Tipo Django | Restricción | Justificación |
|---|---|---|---|
| id | BigAutoField | PK, auto | |
| cliente | ForeignKey(Cliente) | PROTECT | Decisión D-03 |
| fecha | DateTimeField | auto_now_add | Fecha de creación inmutable |
| total | Propiedad calculada | NO es campo de BD | Decisión D-04 |

## Entidad 6 — DetalleVenta

| Atributo | Tipo Django | Restricción | Justificación |
|---|---|---|---|
| id | BigAutoField | PK, auto | |
| venta | ForeignKey(Venta) | CASCADE | Si se borra la Venta, se borran sus detalles |
| producto | ForeignKey(Producto) | PROTECT | Decisión D-05 |
| cantidad | PositiveIntegerField | mayor o igual a 1 | No puede haber 0 unidades |
| precio_unitario | DecimalField(10,2) | not null | Decisión D-06 |

## Entidad 7 — Pedido (se implementa en la Espiral 5)

| Atributo | Tipo Django | Restricción | Justificación |
|---|---|---|---|
| id | BigAutoField | PK, auto | |
| numero_pedido | CharField(20) | unique | Código legible: PED-2025-0001 |
| cliente | ForeignKey(Cliente) | PROTECT | Siempre tiene cliente |
| estado | CharField(20) | choices | pendiente/pagado/enviado/cancelado |
| fecha_pedido | DateTimeField | auto_now_add | Cuándo se creó |
| fecha_entrega | DateField | null=True | Opcional |
| total_pagado | DecimalField(10,2) | null=True | Se registra al pagar |

## Entidad 8 — ConfiguracionERP (singleton)

| Atributo | Tipo Django | Restricción | Justificación |
|---|---|---|---|
| id | BigAutoField | PK, auto | |
| nombre_empresa | CharField(200) | not null | Aparece en facturas |
| rfc | CharField(13) | blank=True | RFC del negocio |
| moneda | CharField(3) | default='MXN' | ISO 4217 |
| iva_porcentaje | DecimalField(5,2) | default=16.00 | IVA México |
| logo | ImageField | null=True, blank=True | Logo para facturas |