from django.contrib import admin

from .models import Reserva


@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
	list_display = ('id', 'usuario', 'data_inicio', 'horario_inicio', 'data_fim', 'horario_fim', 'status')
	list_filter = ('status', 'data_inicio')
	search_fields = ('usuario__nome',)
