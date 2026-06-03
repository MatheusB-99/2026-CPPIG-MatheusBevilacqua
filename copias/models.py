from django.db import models


class CopiaChave(models.Model):
	STATUS_CHOICES = [
		('disponivel', 'Disponivel'),
		('emprestada', 'Emprestada'),
		('inativa', 'Inativa'),
	]

	chave = models.ForeignKey(
		'chaves.Chave',
		verbose_name='Chave',
		on_delete=models.CASCADE,
		related_name='copias',
		help_text='Chave de origem da copia',
	)
	status = models.CharField(
		'Status',
		max_length=15,
		choices=STATUS_CHOICES,
		help_text='Status da copia da chave',
	)
	emergencia = models.BooleanField('Emergencia', default=False, help_text='Indica se e copia de emergencia')

	class Meta:
		verbose_name = 'Copia de Chave'
		verbose_name_plural = 'Copias de Chave'
		db_table = 'copias_copiachave'

	def __str__(self):
		return f"Copia {self.id}"

# Create your models here.