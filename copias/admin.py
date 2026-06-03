from django.contrib import admin

from .models import CopiaChave


@admin.register(CopiaChave)
class CopiaChaveAdmin(admin.ModelAdmin):
	list_display = ('id', 'chave', 'status', 'emergencia')
	list_filter = ('status', 'emergencia')
	search_fields = ('chave__sala__predio__endereco',)
