# Ficha de Sistematización — Espiral 3
## ERP Django · Espiral E3: CRUD Web y Autenticación

| Campo | Contenido |
|---|---|
| **Número de espiral** | 3 |
| **Nombre del ciclo** | CRUD Web y Autenticación |
| **Semanas** | W07 – W09 |
| **Fecha de inicio** | 25/10/2026|
| **Fecha de cierre** |26/10/2026|
| **Responsable** | [Mariangel yandel Gomez]
| **Asesor** | MC. Román Fernando López González |

## 1. Objetivo del ciclo
Implementar la interfaz web completa del ERP con vistas de lectura
y escritura, formularios validados, autenticación mediante allauth
y control de acceso por rol (RBAC) con 3 grupos de usuarios.

## 2. Tareas realizadas

| # | Tarea | Estado | Semana |
|---|---|---|---|
| 1 | ListView + DetailView × 4 entidades | ✅ | W07 |
| 2 | 8 templates lista + detalle Fable 5 | ✅ | W07 |
| 3 | select_related anti-N+1 | ✅ | W07 |
| 4 | forms.py × 4 apps (ModelForm) | ✅ | W08 |
| 5 | Create/Update/Delete × 3 entidades | ✅ | W08 |
| 6 | crear_venta (función) | ✅ | W08 |
| 7 | messages flash en CRUD | ✅ | W08 |
| 8 | django-allauth instalado | ✅ | W09 |
| 9 | Templates login/signup Fable 5 | ✅ | W09 |
| 10 | Management command crear_grupos | ✅ | W09 |
| 11 | PermissionRequiredMixin en Delete | ✅ | W09 |
| 12 | @login_required + @permission_required | ✅ | W09 |
| 13 | 10 tests RBAC | ✅ | W09 |

## 3. Evidencias
- URL pública: https://erp-django-utec.onrender.com
- Login funcional: /accounts/login/
- Tests: Ran [NÚMERO] tests → OK
- Grupos: Gerente / Vendedor / Almacén en /admin/

## 4. Criterios de aceptación

| Criterio | Estado |
|---|---|
| GET /productos/ sin login → solo lectura | ✅ |
| GET /productos/eliminar/ sin permiso → 403 | ✅ |
| Gerente → acceso completo | ✅ |
| Vendedor → solo ventas y consulta | ✅ |
| Tests acumulados OK | ✅ |

## 5. Problemas encontrados
1. `crear_grupos` marcaba "Unknown command": la app `core` no estaba
   registrada en INSTALLED_APPS, por lo que Django no detectaba el comando.
2. Error "EmailAddress doesn't declare an explicit app_label": faltaban
   `django.contrib.sites`, `allauth`, `allauth.account` y
   `allauth.socialaccount` en INSTALLED_APPS.
3. Dos tests de W08 (eliminar producto y crear venta) fallaban con
   HTTP 403, porque al agregar permisos en W09 el usuario de prueba
   normal ya no tenía acceso. Se resolvió usando create_superuser
   en el setUp de esos tests.
4. Se intentó ejecutar código de Python en PowerShell/CMD; ese código
   solo funciona dentro de `python manage.py shell`.

## 6. Lecciones aprendidas
1. Un management command solo se detecta si su app está en INSTALLED_APPS.
2. Al agregar permisos a las vistas hay que actualizar los tests
   anteriores que dependían de acceso libre.
3. Revisar siempre INSTALLED_APPS completo antes de correr migrate,
   check y los tests.

## 7. Tiempo total invertido

| Categoría | Horas |
|---|---|
| Diseño | |
| Implementación | |
| Pruebas | |
| Documentación | |
| **Total Espiral 3** | |
