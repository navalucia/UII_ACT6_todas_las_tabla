# --- START OF FILE models.py (MODIFICADO PARA REGISTROCLASE Y MEMBRESIA) ---

from django.db import models

# ==========================================
# MODELO: MEMBRESIA (Nuevo modelo)
# ==========================================
class Membresia(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    costo = models.DecimalField(max_digits=10, decimal_places=2)
    # Acceso podría ser un TextField si es descriptivo, o un CharField con choices
    acceso = models.CharField(max_length=100, help_text="Ej: Acceso total, Solo máquinas, Clases limitadas")
    # Entrenador podría ser un campo booleano si incluye o no entrenador personal
    # O un ManyToMany a Empleado si se asignan entrenadores específicos
    # Por simplicidad, lo haré booleano aquí.
    entrenador_personal_incluido = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre

# ==========================================
# MODELO: CLASE
# ==========================================
class Clase(models.Model):
    nombre_clase = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    horario = models.CharField(max_length=50) # Ejemplo: "Lunes 10:00-11:00"
    duracion_minutos = models.IntegerField()
    cupo_maximo = models.IntegerField()
    nivel_dificultad = models.CharField(
        max_length=20,
        choices=[
            ('Principiante', 'Principiante'),
            ('Intermedio', 'Intermedio'),
            ('Avanzado', 'Avanzado'),
        ],
        default='Principiante'
    )

    def __str__(self):
        return self.nombre_clase

# ==========================================
# MODELO: MIEMBRO (Modificado con ForeignKey a Membresia)
# ==========================================
class Miembro(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    fecha_inscripcion = models.DateField(auto_now_add=True)
    membresia_activa = models.BooleanField(default=True)
    imagen = models.ImageField(upload_to='miembros_imagenes/', blank=True, null=True)

    # ForeignKey a Clase (RELACIÓN 1 A MUCHOS)
    clase_inscrita = models.ForeignKey(
        Clase,
        on_delete=models.SET_NULL,
        related_name='miembros',
        blank=True,
        null=True
    )

    # NUEVO CAMPO: ForeignKey a Membresia (RELACIÓN 1 A MUCHOS)
    # Un Miembro tiene UNA Membresia (o ninguna, por eso blank=True, null=True)
    membresia = models.ForeignKey(
        Membresia,
        on_delete=models.SET_NULL,
        related_name='miembros', # Desde una membresía, puedes obtener todos sus miembros con membresia_instancia.miembros.all()
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

# ==========================================
# MODELO: EMPLEADO
# ==========================================
class Empleado(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    fecha_contratacion = models.DateField(auto_now_add=True)
    puesto = models.CharField(max_length=100)
    salario = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    
    # ManyToManyField a Clase (RELACIÓN MUCHOS A MUCHOS)
    clases_impartidas = models.ManyToManyField(
        Clase,
        related_name='instructores',
        blank=True
    )

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.puesto})"

# ==========================================
# MODELO: REGISTROCLASE (Nuevo modelo)
# ==========================================
class RegistroClase(models.Model):
    # ForeignKeys a Miembro y Clase
    miembro = models.ForeignKey(
        Miembro,
        on_delete=models.CASCADE, # Si se elimina un miembro, sus registros de clase también se eliminan
        related_name='registros_clase' # Desde un miembro, puedes obtener sus registros con miembro_instancia.registros_clase.all()
    )
    clase = models.ForeignKey(
        Clase,
        on_delete=models.CASCADE, # Si se elimina una clase, sus registros también se eliminan
        related_name='registros_clase' # Desde una clase, puedes obtener sus registros con clase_instancia.registros_clase.all()
    )
    fecha_registro = models.DateField(auto_now_add=True)
    asistencia = models.BooleanField(default=False)
    calificacion_miembro = models.IntegerField(
        blank=True,
        null=True,
        choices=[(i, str(i)) for i in range(1, 6)], # Calificación del 1 al 5
        help_text="Calificación del miembro para esta clase (1-5)"
    )

    class Meta:
        # Asegura que un miembro no pueda registrarse dos veces en la misma clase el mismo día
        unique_together = ('miembro', 'clase', 'fecha_registro')
        verbose_name = "Registro de Clase"
        verbose_name_plural = "Registros de Clases"

    def __str__(self):
        return f"Registro de {self.miembro.nombre} en {self.clase.nombre_clase} el {self.fecha_registro}"

# --- END OF FILE models.py (MODIFICADO PARA REGISTROCLASE Y MEMBRESIA) ---