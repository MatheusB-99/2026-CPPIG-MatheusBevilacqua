from django.contrib import admin

from .models import Sala, SalaComunitaria, SalaExclusiva


@admin.register(Sala)
class SalaAdmin(admin.ModelAdmin):
	list_display = ('id', 'predio')
	search_fields = ('predio__endereco',)


@admin.register(SalaExclusiva)
class SalaExclusivaAdmin(admin.ModelAdmin):
	list_display = ('id', 'predio')
	search_fields = ('predio__endereco',)


@admin.register(SalaComunitaria)
class SalaComunitariaAdmin(admin.ModelAdmin):
	list_display = ('id', 'predio')
	search_fields = ('predio__endereco',)
