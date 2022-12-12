from django.contrib import admin
from .models import Evento, Lugar, eConnectUser

# Register your models here.
#admin.site.register(Evento)
#admin.site.register(Lugar)
admin.site.register(eConnectUser)


@admin.register(Lugar)
class LugarAdmin(admin.ModelAdmin):
    list_display = ('Nombre', 'dirección', 'teléfono')
    ordering = ('Nombre', )
    search_fields = ('Nombre', 'dirección')


@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    fields = (('Nombre', 'Lugar'), 'Evento_fecha', 'gestor', 'Descripción', 'Asistentes', 'approved')
    list_display = ('Nombre', 'Lugar', 'Evento_fecha')
    ordering = ('Evento_fecha',)
    search_fields = ('Nombre', 'Lugar')
    list_filter = ('Evento_fecha', 'Lugar')

