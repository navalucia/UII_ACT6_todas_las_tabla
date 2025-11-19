from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio_gym, name='inicio_gym'),

    # URLs para Miembros
    path('miembros/', views.ver_miembros, name='ver_miembros'),
    path('miembros/agregar/', views.agregar_miembro, name='agregar_miembro'),
    path('miembros/actualizar/<int:pk>/', views.actualizar_miembro, name='actualizar_miembro'),
    path('miembros/borrar/<int:pk>/', views.borrar_miembro, name='borrar_miembro'),

    # URLs para Clases
    path('clases/', views.ver_clases, name='ver_clases'),
    path('clases/agregar/', views.agregar_clase, name='agregar_clase'),
    path('clases/actualizar/<int:pk>/', views.actualizar_clase, name='actualizar_clase'),
    path('clases/borrar/<int:pk>/', views.borrar_clase, name='borrar_clase'),

    # URLs para Empleados
    path('empleados/', views.ver_empleados, name='ver_empleados'),
    path('empleados/agregar/', views.agregar_empleado, name='agregar_empleado'),
    path('empleados/actualizar/<int:pk>/', views.actualizar_empleado, name='actualizar_empleado'),
    path('empleados/borrar/<int:pk>/', views.borrar_empleado, name='borrar_empleado'),

    # URLs para Membresías
    path('membresias/', views.ver_membresias, name='ver_membresias'),
    path('membresias/agregar/', views.agregar_membresia, name='agregar_membresia'),
    path('membresias/actualizar/<int:pk>/', views.actualizar_membresia, name='actualizar_membresia'),
    path('membresias/borrar/<int:pk>/', views.borrar_membresia, name='borrar_membresia'),

    # --- AQUÍ ESTABA EL ERROR, AHORA ESTÁ CORREGIDO ---
    # Usamos 'registros-clase' (con guion) para que coincida con tu navegador
    path('registros-clase/', views.ver_registros_clase, name='ver_registros_clase'),
    path('registros-clase/agregar/', views.agregar_registro_clase, name='agregar_registro_clase'),
    path('registros-clase/actualizar/<int:pk>/', views.actualizar_registro_clase, name='actualizar_registro_clase'),
    path('registros-clase/borrar/<int:pk>/', views.borrar_registro_clase, name='borrar_registro_clase'),
]