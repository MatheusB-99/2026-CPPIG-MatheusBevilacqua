from django.db import models


class Sala(models.Model):
    class TipoSala(models.TextChoices):
        COMUNITARIA = 'comunitaria', 'Comunitaria'
        EXCLUSIVA = 'exclusiva', 'Exclusiva'

    predio = models.ForeignKey(
        'predios.Predio',
        verbose_name='Predio',
        on_delete=models.CASCADE,
        related_name='salas',
        help_text='Predio ao qual a sala pertence',
    )

    class Meta:
        verbose_name = 'Sala'
        verbose_name_plural = 'Salas'
        db_table = 'salas_sala'

    @property
    def tipo_sala(self):
        if SalaComunitaria.objects.filter(pk=self.pk).exists():
            return self.TipoSala.COMUNITARIA
        if SalaExclusiva.objects.filter(pk=self.pk).exists():
            return self.TipoSala.EXCLUSIVA
        return ''

    @property
    def tipo_sala_label(self):
        return dict(self.TipoSala.choices).get(self.tipo_sala, 'Nao definido')

    @property
    def eh_comunitaria(self):
        return self.tipo_sala == self.TipoSala.COMUNITARIA

    @property
    def eh_exclusiva(self):
        return self.tipo_sala == self.TipoSala.EXCLUSIVA

    def __str__(self):
        return f"Sala {self.id}"


class SalaExclusiva(Sala):
    class Meta:
        verbose_name = 'Sala Exclusiva'
        verbose_name_plural = 'Salas Exclusivas'
        db_table = 'salas_salaexclusiva'


class SalaComunitaria(Sala):
    class Meta:
        verbose_name = 'Sala Comunitaria'
        verbose_name_plural = 'Salas Comunitarias'
        db_table = 'salas_salacomunitaria'

# Create your models here.
