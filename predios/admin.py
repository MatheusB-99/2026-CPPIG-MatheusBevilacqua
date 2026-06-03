from django.contrib import admin

from .models import Predio


@admin.register(Predio)
class PredioAdmin(admin.ModelAdmin):
	list_display = ('id', 'endereco')
	search_fields = ('endereco',)
