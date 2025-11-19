# app_gym/views.py

from django.shortcuts import render, redirect, get_object_or_404
from .models import Miembro, Clase, Empleado, Membresia, RegistroClase # Importar nuevos modelos
from django.contrib import messages
from django.http import HttpResponse
from datetime import date # Para usar en RegistroClase


def inicio_gym(request):
    context = {}
    return render(request, 'app_gym/inicio.html', context)

# --- VISTAS PARA MIEMBROS ---

def agregar_miembro(request):
    clases_disponibles = Clase.objects.all().order_by('nombre_clase')
    membresias_disponibles = Membresia.objects.all().order_by('nombre') # Obtener membresías
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        fecha_nacimiento = request.POST.get('fecha_nacimiento')
        email = request.POST.get('email')
        telefono = request.POST.get('telefono', '')
        membresia_activa = request.POST.get('membresia_activa') == 'on'
        imagen = request.FILES.get('imagen')
        clase_id = request.POST.get('clase_inscrita')
        membresia_id = request.POST.get('membresia') # Obtener el ID de la membresía seleccionada

        clase_inscrita_obj = None
        if clase_id:
            clase_inscrita_obj = get_object_or_404(Clase, pk=clase_id)

        membresia_obj = None
        if membresia_id: # Solo intenta obtener la membresía si se seleccionó una
            membresia_obj = get_object_or_404(Membresia, pk=membresia_id)

        try:
            Miembro.objects.create(
                nombre=nombre,
                apellido=apellido,
                fecha_nacimiento=fecha_nacimiento,
                email=email,
                telefono=telefono,
                membresia_activa=membresia_activa,
                imagen=imagen,
                clase_inscrita=clase_inscrita_obj,
                membresia=membresia_obj # Asignar el objeto Membresia
            )
            messages.success(request, 'Miembro agregado exitosamente!')
            return redirect('ver_miembros')
        except Exception as e:
            messages.error(request, f"Error al agregar el miembro: {e}")

    context = {
        'clases_disponibles': clases_disponibles,
        'membresias_disponibles': membresias_disponibles # Pasar membresías al contexto
    }
    return render(request, 'miembros/agregar_miembros.html', context)


def ver_miembros(request):
    try:
        # Usar select_related para traer la información de la clase y la membresía en la misma consulta
        miembros = Miembro.objects.all().select_related('clase_inscrita', 'membresia').order_by('apellido', 'nombre')
        if not miembros.exists():
            messages.info(request, "No hay miembros registrados para mostrar. ¡Añade algunos!")
        context = {'miembros': miembros}
        return render(request, 'miembros/ver_miembros.html', context)
    except Exception as e:
        messages.error(request, f"Ocurrió un error al cargar los miembros: {e}")
        return render(request, 'app_gym/inicio.html', {'error_message': str(e)})


def actualizar_miembro(request, pk):
    miembro = get_object_or_404(Miembro, pk=pk)
    clases_disponibles = Clase.objects.all().order_by('nombre_clase')
    membresias_disponibles = Membresia.objects.all().order_by('nombre') # Obtener membresías

    if request.method == 'POST':
        miembro.nombre = request.POST.get('nombre')
        miembro.apellido = request.POST.get('apellido')
        miembro.fecha_nacimiento = request.POST.get('fecha_nacimiento')
        miembro.email = request.POST.get('email')
        miembro.telefono = request.POST.get('telefono', '')
        miembro.membresia_activa = request.POST.get('membresia_activa') == 'on'

        clase_id = request.POST.get('clase_inscrita')
        if clase_id:
            miembro.clase_inscrita = get_object_or_404(Clase, pk=clase_id)
        else:
            miembro.clase_inscrita = None

        membresia_id = request.POST.get('membresia') # Obtener el ID de la membresía seleccionada
        if membresia_id:
            miembro.membresia = get_object_or_404(Membresia, pk=membresia_id)
        else:
            miembro.membresia = None # Si no se selecciona ninguna, se pone a NULL

        if 'imagen' in request.FILES:
            if miembro.imagen:
                miembro.imagen.delete(save=False)
            miembro.imagen = request.FILES['imagen']
        elif 'borrar_imagen' in request.POST:
            if miembro.imagen:
                miembro.imagen.delete(save=False)
            miembro.imagen = None

        try:
            miembro.save()
            messages.info(request, 'Miembro actualizado exitosamente!')
            return redirect('ver_miembros')
        except Exception as e:
            messages.error(request, f"Error al actualizar el miembro: {e}")

    context = {
        'miembro': miembro,
        'clases_disponibles': clases_disponibles,
        'membresias_disponibles': membresias_disponibles # Pasar membresías al contexto
    }
    return render(request, 'miembros/actualizar_miembros.html', context)


def borrar_miembro(request, pk):
    miembro = get_object_or_404(Miembro, pk=pk)
    if request.method == 'POST':
        if miembro.imagen:
            miembro.imagen.delete()
        miembro.delete()
        messages.error(request, 'Miembro eliminado correctamente.')
        return redirect('ver_miembros')
    context = {'miembro': miembro}
    return render(request, 'miembros/confirmar_borrar_miembros.html', context)


# --- VISTAS PARA CLASES ---

def agregar_clase(request):
    if request.method == 'POST':
        nombre_clase = request.POST.get('nombre_clase')
        descripcion = request.POST.get('descripcion')
        horario = request.POST.get('horario')
        duracion_minutos = request.POST.get('duracion_minutos')
        cupo_maximo = request.POST.get('cupo_maximo')
        nivel_dificultad = request.POST.get('nivel_dificultad')

        try:
            Clase.objects.create(
                nombre_clase=nombre_clase,
                descripcion=descripcion,
                horario=horario,
                duracion_minutos=int(duracion_minutos),
                cupo_maximo=int(cupo_maximo),
                nivel_dificultad=nivel_dificultad,
            )
            messages.success(request, 'Clase agregada exitosamente!')
            return redirect('ver_clases')
        except ValueError:
            messages.error(request, 'Error: Duración y cupo deben ser números enteros.')
        except Exception as e:
            messages.error(request, f'Error al agregar la clase: {e}')

    return render(request, 'clases/agregar_clase.html')


def ver_clases(request):
    try:
        clases = Clase.objects.all().order_by('horario', 'nombre_clase')
        if not clases.exists():
            messages.info(request, "No hay clases registradas para mostrar. ¡Añade algunas!")
        context = {'clases': clases}
        return render(request, 'clases/ver_clases.html', context)
    except Exception as e:
        messages.error(request, f"Ocurrió un error al cargar las clases: {e}")
        return render(request, 'app_gym/inicio.html', {'error_message': str(e)})


def actualizar_clase(request, pk):
    clase = get_object_or_404(Clase, pk=pk)
    
    if request.method == 'POST':
        nombre_clase_post = request.POST.get('nombre_clase')
        descripcion_post = request.POST.get('descripcion')
        horario_post = request.POST.get('horario')
        duracion_minutos_post_str = request.POST.get('duracion_minutos')
        cupo_maximo_post_str = request.POST.get('cupo_maximo')
        nivel_dificultad_post = request.POST.get('nivel_dificultad')
        
        try:
            clase.nombre_clase = nombre_clase_post
            clase.descripcion = descripcion_post
            clase.horario = horario_post
            clase.nivel_dificultad = nivel_dificultad_post
            
            clase.duracion_minutos = int(duracion_minutos_post_str)
            clase.cupo_maximo = int(cupo_maximo_post_str)
            
            clase.save()
            messages.info(request, 'Clase actualizada exitosamente!')
            return redirect('ver_clases')
        except ValueError as ve:
            messages.error(request, f'Error: Duración y cupo deben ser números enteros válidos. Detalle: {ve}')
        except Exception as e:
            messages.error(request, f'Error inesperado al actualizar la clase: {e}')

    context = {
        'clase': clase,
        'niveles_dificultad': Clase.nivel_dificultad.field.choices
    }
    return render(request, 'clases/actualizar_clase.html', context)


def borrar_clase(request, pk):
    clase = get_object_or_404(Clase, pk=pk)
    if request.method == 'POST':
        clase.delete()
        messages.error(request, 'Clase eliminada correctamente.')
        return redirect('ver_clases')
    context = {'clase': clase}
    return render(request, 'clases/confirmar_borrar_clase.html', context)


# --- VISTAS PARA EMPLEADOS (Nuevas) ---

def agregar_empleado(request):
    clases_disponibles = Clase.objects.all().order_by('nombre_clase')
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        puesto = request.POST.get('puesto')
        salario = request.POST.get('salario')
        email = request.POST.get('email')
        telefono = request.POST.get('telefono', '')
        clases_ids = request.POST.getlist('clases_impartidas') # getlist para ManyToMany

        try:
            empleado = Empleado.objects.create(
                nombre=nombre,
                apellido=apellido,
                puesto=puesto,
                salario=float(salario) if salario else None,
                email=email,
                telefono=telefono,
            )
            # Asignar las clases ManyToMany
            if clases_ids:
                clases_seleccionadas = Clase.objects.filter(pk__in=clases_ids)
                empleado.clases_impartidas.set(clases_seleccionadas) # set() para ManyToMany

            messages.success(request, 'Empleado agregado exitosamente!')
            return redirect('ver_empleados')
        except ValueError:
            messages.error(request, 'Error: El salario debe ser un número válido.')
        except Exception as e:
            messages.error(request, f'Error al agregar el empleado: {e}')

    context = {'clases_disponibles': clases_disponibles}
    return render(request, 'empleados/agregar_empleado.html', context)


def ver_empleados(request):
    try:
        # Usar prefetch_related para ManyToMany
        empleados = Empleado.objects.all().prefetch_related('clases_impartidas').order_by('apellido', 'nombre')
        if not empleados.exists():
            messages.info(request, "No hay empleados registrados para mostrar. ¡Añade algunos!")
        context = {'empleados': empleados}
        return render(request, 'empleados/ver_empleados.html', context)
    except Exception as e:
        messages.error(request, f"Ocurrió un error al cargar los empleados: {e}")
        return render(request, 'app_gym/inicio.html', {'error_message': str(e)})


def actualizar_empleado(request, pk):
    empleado = get_object_or_404(Empleado, pk=pk)
    clases_disponibles = Clase.objects.all().order_by('nombre_clase')

    if request.method == 'POST':
        empleado.nombre = request.POST.get('nombre')
        empleado.apellido = request.POST.get('apellido')
        empleado.puesto = request.POST.get('puesto')
        salario_str = request.POST.get('salario')
        empleado.email = request.POST.get('email')
        empleado.telefono = request.POST.get('telefono', '')
        clases_ids = request.POST.getlist('clases_impartidas')

        try:
            empleado.salario = float(salario_str) if salario_str else None
            empleado.save()

            # Actualizar las clases ManyToMany
            if clases_ids:
                clases_seleccionadas = Clase.objects.filter(pk__in=clases_ids)
                empleado.clases_impartidas.set(clases_seleccionadas)
            else:
                empleado.clases_impartidas.clear()

            messages.info(request, 'Empleado actualizado exitosamente!')
            return redirect('ver_empleados')
        except ValueError:
            messages.error(request, 'Error: El salario debe ser un número válido.')
        except Exception as e:
            messages.error(request, f'Error inesperado al actualizar el empleado: {e}')

    clases_actualmente_impartidas_ids = empleado.clases_impartidas.values_list('id', flat=True)

    context = {
        'empleado': empleado,
        'clases_disponibles': clases_disponibles,
        'clases_actualmente_impartidas_ids': list(clases_actualmente_impartidas_ids)
    }
    return render(request, 'empleados/actualizar_empleado.html', context)


def borrar_empleado(request, pk):
    empleado = get_object_or_404(Empleado, pk=pk)
    if request.method == 'POST':
        empleado.delete()
        messages.error(request, 'Empleado eliminado correctamente.')
        return redirect('ver_empleados')
    context = {'empleado': empleado}
    return render(request, 'empleados/confirmar_borrar_empleado.html', context)


# --- VISTAS PARA MEMBRESIAS (Nuevas) ---

def agregar_membresia(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion', '')
        costo = request.POST.get('costo')
        acceso = request.POST.get('acceso')
        entrenador_personal_incluido = request.POST.get('entrenador_personal_incluido') == 'on'

        try:
            Membresia.objects.create(
                nombre=nombre,
                descripcion=descripcion,
                costo=float(costo),
                acceso=acceso,
                entrenador_personal_incluido=entrenador_personal_incluido
            )
            messages.success(request, 'Membresía agregada exitosamente!')
            return redirect('ver_membresias')
        except ValueError:
            messages.error(request, 'Error: El costo debe ser un número válido.')
        except Exception as e:
            messages.error(request, f'Error al agregar la membresía: {e}')

    return render(request, 'membresias/agregar_membresia.html')


def ver_membresias(request):
    try:
        membresias = Membresia.objects.all().order_by('costo', 'nombre')
        if not membresias.exists():
            messages.info(request, "No hay membresías registradas para mostrar. ¡Añade algunas!")
        context = {'membresias': membresias}
        return render(request, 'membresias/ver_membresias.html', context)
    except Exception as e:
        messages.error(request, f"Ocurrió un error al cargar las membresías: {e}")
        return render(request, 'app_gym/inicio.html', {'error_message': str(e)})


def actualizar_membresia(request, pk):
    membresia = get_object_or_404(Membresia, pk=pk)

    if request.method == 'POST':
        membresia.nombre = request.POST.get('nombre')
        membresia.descripcion = request.POST.get('descripcion', '')
        costo_str = request.POST.get('costo')
        membresia.acceso = request.POST.get('acceso')
        membresia.entrenador_personal_incluido = request.POST.get('entrenador_personal_incluido') == 'on'

        try:
            membresia.costo = float(costo_str) if costo_str else None
            membresia.save()
            messages.info(request, 'Membresía actualizada exitosamente!')
            return redirect('ver_membresias')
        except ValueError:
            messages.error(request, 'Error: El costo debe ser un número válido.')
        except Exception as e:
            messages.error(request, f'Error inesperado al actualizar la membresía: {e}')

    context = {'membresia': membresia}
    return render(request, 'membresias/actualizar_membresia.html', context)


def borrar_membresia(request, pk):
    membresia = get_object_or_404(Membresia, pk=pk)
    if request.method == 'POST':
        membresia.delete()
        messages.error(request, 'Membresía eliminada correctamente.')
        return redirect('ver_membresias')
    context = {'membresia': membresia}
    return render(request, 'membresias/confirmar_borrar_membresia.html', context)


# --- VISTAS PARA REGISTRO DE CLASES (Nuevas) ---

def agregar_registro_clase(request):
    miembros_disponibles = Miembro.objects.all().order_by('apellido', 'nombre')
    clases_disponibles = Clase.objects.all().order_by('nombre_clase')

    if request.method == 'POST':
        miembro_id = request.POST.get('miembro')
        clase_id = request.POST.get('clase')
        asistencia = request.POST.get('asistencia') == 'on'
        calificacion_miembro = request.POST.get('calificacion_miembro')
        fecha_registro_str = request.POST.get('fecha_registro') # Permitir seleccionar fecha para registros pasados

        miembro_obj = get_object_or_404(Miembro, pk=miembro_id)
        clase_obj = get_object_or_404(Clase, pk=clase_id)

        try:
            # Convertir la fecha_registro a objeto date
            fecha_registro_obj = date.fromisoformat(fecha_registro_str) if fecha_registro_str else date.today()

            # Asegurarse de que no haya un registro duplicado para el mismo miembro, clase y fecha
            if RegistroClase.objects.filter(miembro=miembro_obj, clase=clase_obj, fecha_registro=fecha_registro_obj).exists():
                messages.warning(request, f"Ya existe un registro para {miembro_obj.nombre} en {clase_obj.nombre_clase} el {fecha_registro_obj}.")
                return redirect('agregar_registro_clase')

            RegistroClase.objects.create(
                miembro=miembro_obj,
                clase=clase_obj,
                asistencia=asistencia,
                calificacion_miembro=int(calificacion_miembro) if calificacion_miembro else None,
                fecha_registro=fecha_registro_obj
            )
            messages.success(request, 'Registro de clase agregado exitosamente!')
            return redirect('ver_registros_clase')
        except ValueError:
            messages.error(request, 'Error: La calificación debe ser un número entero.')
        except Exception as e:
            messages.error(request, f'Error al agregar el registro de clase: {e}')

    context = {
        'miembros_disponibles': miembros_disponibles,
        'clases_disponibles': clases_disponibles,
        'today': date.today().isoformat() # Pasa la fecha actual para el campo de fecha por defecto
    }
    return render(request, 'registro_clase/agregar_registro_clase.html', context)


def ver_registros_clase(request):
    try:
        # Usar select_related para traer la información de miembro y clase
        registros = RegistroClase.objects.all().select_related('miembro', 'clase').order_by('-fecha_registro', 'clase__nombre_clase', 'miembro__apellido')
        if not registros.exists():
            messages.info(request, "No hay registros de clases para mostrar. ¡Añade algunos!")
        context = {'registros': registros}
        return render(request, 'registro_clase/ver_registros_clase.html', context)
    except Exception as e:
        messages.error(request, f"Ocurrió un error al cargar los registros de clase: {e}")
        return render(request, 'app_gym/inicio.html', {'error_message': str(e)})


def actualizar_registro_clase(request, pk):
    registro = get_object_or_404(RegistroClase, pk=pk)
    miembros_disponibles = Miembro.objects.all().order_by('apellido', 'nombre')
    clases_disponibles = Clase.objects.all().order_by('nombre_clase')

    if request.method == 'POST':
        miembro_id = request.POST.get('miembro')
        clase_id = request.POST.get('clase')
        asistencia = request.POST.get('asistencia') == 'on'
        calificacion_miembro_str = request.POST.get('calificacion_miembro')
        fecha_registro_str = request.POST.get('fecha_registro')

        miembro_obj = get_object_or_404(Miembro, pk=miembro_id)
        clase_obj = get_object_or_404(Clase, pk=clase_id)

        try:
            fecha_registro_obj = date.fromisoformat(fecha_registro_str) if fecha_registro_str else registro.fecha_registro

            # Antes de guardar, verificar si la nueva combinación de miembro, clase y fecha ya existe en otro registro
            if RegistroClase.objects.filter(miembro=miembro_obj, clase=clase_obj, fecha_registro=fecha_registro_obj).exclude(pk=pk).exists():
                messages.warning(request, f"Ya existe un registro para {miembro_obj.nombre} en {clase_obj.nombre_clase} el {fecha_registro_obj}. No se puede duplicar.")
                return redirect('actualizar_registro_clase', pk=pk)

            registro.miembro = miembro_obj
            registro.clase = clase_obj
            registro.asistencia = asistencia
            registro.calificacion_miembro = int(calificacion_miembro_str) if calificacion_miembro_str else None
            registro.fecha_registro = fecha_registro_obj
            registro.save()
            messages.info(request, 'Registro de clase actualizado exitosamente!')
            return redirect('ver_registros_clase')
        except ValueError:
            messages.error(request, 'Error: La calificación debe ser un número entero.')
        except Exception as e:
            messages.error(request, f'Error inesperado al actualizar el registro de clase: {e}')

    context = {
        'registro': registro,
        'miembros_disponibles': miembros_disponibles,
        'clases_disponibles': clases_disponibles,
        'calificaciones_choices': RegistroClase.calificacion_miembro.field.choices
    }
    return render(request, 'registro_clase/actualizar_registro_clase.html', context)


def borrar_registro_clase(request, pk):
    registro = get_object_or_404(RegistroClase, pk=pk)
    if request.method == 'POST':
        registro.delete()
        messages.error(request, 'Registro de clase eliminado correctamente.')
        return redirect('ver_registros_clase')
    context = {'registro': registro}
    return render(request, 'registro_clase/confirmar_borrar_registro_clase.html', context)