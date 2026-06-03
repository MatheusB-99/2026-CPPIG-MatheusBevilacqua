from django.contrib import admin

from .models import Chave


@admin.register(Chave)
class ChaveAdmin(admin.ModelAdmin):
	list_display = ('id', 'tipo', 'sala', 'predio')
	list_filter = ('tipo',)
	search_fields = ('sala__predio__endereco', 'predio__endereco')
