from django.db import models


class Usuario(models.Model):
	class TipoUsuario(models.TextChoices):
		ADMINISTRADOR = 'administrador', 'Administrador'
		USUARIO_NORMAL = 'usuario_normal', 'Usuario normal'

	nome = models.CharField('Nome', max_length=120, help_text='Nome do usuario')
	email = models.EmailField('Email', unique=True, help_text='Email do usuario')
	tipo = models.CharField(
		'Tipo',
		max_length=20,
		choices=TipoUsuario.choices,
		help_text='Tipo de usuario',
	)
	senha = models.CharField('Senha', max_length=128, help_text='Senha do usuario')
	cpf = models.CharField('CPF', max_length=14, unique=True, help_text='CPF do usuario')

	class Meta:
		verbose_name = 'Usuario'
		verbose_name_plural = 'Usuarios'
		db_table = 'usuarios_usuario'

	def __str__(self):
		return self.nome
