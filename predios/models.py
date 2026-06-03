from django.db import models


class Predio(models.Model):
    endereco = models.CharField('Endereco', max_length=255, help_text='Endereco do predio')

    class Meta:
        verbose_name = 'Predio'
        verbose_name_plural = 'Predios'
        db_table = 'predios_predio'

    def __str__(self):
        return self.endereco

# Create your models here.
