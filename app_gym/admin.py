from django.contrib import admin
from .models import Miembro, Clase, Empleado

# Registra tus modelos aquí.
admin.site.register(Miembro)
admin.site.register(Clase) # Solo para adorno en el admin
admin.site.register(Empleado) # Solo 