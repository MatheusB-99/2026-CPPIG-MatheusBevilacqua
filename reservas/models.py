from django.db import models


class Reserva(models.Model):
	STATUS_CHOICES = [
		('aberta', 'Aberta'),
		('confirmada', 'Confirmada'),
		('cancelada', 'Cancelada'),
	]
	usuario = models.ForeignKey(
		'usuarios.Usuario',
		verbose_name='Usuario',
		on_delete=models.CASCADE,
		related_name='reservas_modulo',
		help_text='Usuario da reserva',
	)
	copia_chave = models.ForeignKey(
		'copias.CopiaChave',
		verbose_name='Copia da chave',
		on_delete=models.PROTECT,
		related_name='reservas',
		null=True,
		blank=True,
		help_text='Copia de chave vinculada a reserva',
	)
	data_inicio = models.DateField('Data de início', null=True, blank=True, help_text='Data de início da reserva')
	horario_inicio = models.TimeField('Horário de início', null=True, blank=True, help_text='Horário de início da reserva')
	data_fim = models.DateField('Data de término', null=True, blank=True, help_text='Data de término da reserva')
	horario_fim = models.TimeField('Horário de término', null=True, blank=True, help_text='Horário de término da reserva')
	data = models.DateField('Data', null=True, blank=True, help_text='Data da reserva')
	horario = models.TimeField('Horario', null=True, blank=True, help_text='Horario da reserva')
	status = models.CharField(
		'Status',
		max_length=15,
		choices=STATUS_CHOICES,
		help_text='Status da reserva',
	)

	class Meta:
		verbose_name = 'Reserva'
		verbose_name_plural = 'Reservas'
		db_table = 'reservas_reserva'

	def save(self, *args, **kwargs):
		if self.data_inicio and not self.data:
			self.data = self.data_inicio
		if self.horario_inicio and not self.horario:
			self.horario = self.horario_inicio
		super().save(*args, **kwargs)

	def __str__(self):
		return f"Reserva {self.id}"

# Create your models here.
