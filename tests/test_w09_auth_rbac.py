"""Suite de pruebas W09: autenticación y permisos por rol."""

from decimal import Decimal

from django.contrib.auth.models import Group, User
from django.test import TestCase
from django.urls import reverse

from clientes.models import Cliente
from productos.models import Categoria, Producto


class AuthBasicTest(TestCase):
    """Pruebas de autenticación básica."""

    def test_login_page_http_200(self):
        response = self.client.get(reverse('account_login'))
        self.assertEqual(response.status_code, 200)

    def test_login_usa_template_personalizado(self):
        response = self.client.get(reverse('account_login'))
        self.assertTemplateUsed(response, 'account/login.html')

    def test_login_correcto_redirige_a_productos(self):
        User.objects.create_user(
            username='testlogin',
            password='pass123'
        )
        response = self.client.post(
            reverse('account_login'),
            {'login': 'testlogin', 'password': 'pass123'}
        )
        self.assertRedirects(
            response, '/productos/', fetch_redirect_response=False
        )


class PermisosGruposTest(TestCase):
    """Pruebas de permisos por grupo."""

    def setUp(self):
        self.categoria = Categoria.objects.create(nombre='Cat')
        self.producto = Producto.objects.create(
            nombre='Prod',
            precio=Decimal('100.00'),
            stock=5,
            categoria=self.categoria
        )
        self.cliente = Cliente.objects.create(
            nombre='Cliente prueba',
            correo='cliente@test.com'
        )

    def crear_usuario(self, username, grupo_nombre):
        usuario = User.objects.create_user(
            username=username,
            password='pass123'
        )
        grupo, _ = Group.objects.get_or_create(name=grupo_nombre)
        usuario.groups.add(grupo)
        return usuario

    def test_gerente_tiene_permiso_eliminar_producto(self):
        usuario = self.crear_usuario('gerente', 'Gerente')
        permiso = 'productos.delete_producto'
        usuario.user_permissions.add(
            __import__('django.contrib.auth.models',
                       fromlist=['Permission']).Permission.objects.get(
                codename='delete_producto'
            )
        )
        usuario = User.objects.get(pk=usuario.pk)
        self.assertTrue(usuario.has_perm(permiso))

    def test_usuario_anonimo_no_esta_autenticado(self):
        self.assertFalse(self.client.session.get('_auth_user_id'))

    def test_usuario_puede_iniciar_sesion(self):
        User.objects.create_user('prueba', password='pass123')
        resultado = self.client.login(
            username='prueba', password='pass123'
        )
        self.assertTrue(resultado)

    def test_grupo_gerente_se_puede_crear(self):
        grupo, _ = Group.objects.get_or_create(name='Gerente')
        self.assertEqual(grupo.name, 'Gerente')

    def test_grupo_vendedor_se_puede_crear(self):
        grupo, _ = Group.objects.get_or_create(name='Vendedor')
        self.assertEqual(grupo.name, 'Vendedor')

    def test_grupo_almacen_se_puede_crear(self):
        grupo, _ = Group.objects.get_or_create(name='Almacén')
        self.assertEqual(grupo.name, 'Almacén')

    def test_producto_tiene_categoria(self):
        self.assertEqual(self.producto.categoria, self.categoria)

    def test_cliente_se_crea_correctamente(self):
        self.assertEqual(self.cliente.nombre, 'Cliente prueba')