from django.contrib import admin

from .models import Emprestimo


@admin.register(Emprestimo)
class EmprestimoAdmin(admin.ModelAdmin):
	list_display = (
		'id',
		'usuario',
		'copia_chave',
		'data_retirada',
		'data_prevista',
		'data_devolucao',
		'status',
	)
	list_filter = ('status', 'data_retirada')
	search_fields = ('usuario__nome', 'copia_chave__id')
