from django.core.exceptions import ValidationError
from django.db import models


class Chave(models.Model):
    class TipoChave(models.TextChoices):
        SALA = 'sala', 'Chave de sala'
        PREDIO = 'predio', 'Chave de predio'

    tipo = models.CharField(
        'Tipo',
        max_length=10,
        choices=TipoChave.choices,
        default=TipoChave.SALA,
        help_text='Define se a chave pertence a sala ou ao predio',
    )
    sala = models.ForeignKey(
        'salas.Sala',
        verbose_name='Sala',
        on_delete=models.CASCADE,
        related_name='chaves',
        null=True,
        blank=True,
        help_text='Sala da chave',
    )
    predio = models.ForeignKey(
        'predios.Predio',
        verbose_name='Predio',
        on_delete=models.CASCADE,
        related_name='chaves_predio',
        null=True,
        blank=True,
        help_text='Predio da chave quando for chave geral',
    )

    class Meta:
        verbose_name = 'Chave'
        verbose_name_plural = 'Chaves'
        db_table = 'chaves_chave'
        ordering = ['id']

    def clean(self):
        super().clean()
        if self.tipo == self.TipoChave.SALA:
            if not self.sala_id:
                raise ValidationError({'sala': 'Informe a sala para chave do tipo sala.'})
            if self.predio_id:
                raise ValidationError({'predio': 'Nao informe predio para chave do tipo sala.'})

        if self.tipo == self.TipoChave.PREDIO:
            if not self.predio_id:
                raise ValidationError({'predio': 'Informe o predio para chave do tipo predio.'})
            if self.sala_id:
                raise ValidationError({'sala': 'Nao informe sala para chave do tipo predio.'})

    @property
    def pode_emprestar(self):
        return self.tipo == self.TipoChave.SALA

    def __str__(self):
        if self.tipo == self.TipoChave.PREDIO and self.predio_id:
            return f"Chave Predio {self.predio.endereco}"
        if self.sala_id:
            return f"Chave Sala {self.sala.id}"
        return f"Chave {self.id}"

# Create your models here.
