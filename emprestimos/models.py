from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.functions import Upper


class Emprestimo(models.Model):
    class StatusEmprestimo(models.TextChoices):
        ABERTO = 'aberto', 'Aberto'
        DEVOLVIDO = 'devolvido', 'Devolvido'
        ATRASADO = 'atrasado', 'Atrasado'

    usuario = models.ForeignKey(
        'usuarios.Usuario',
        verbose_name='Usuario',
        on_delete=models.CASCADE,
        related_name='emprestimos',
        help_text='Usuario que realizou o emprestimo',
    )
    copia_chave = models.ForeignKey(
        'copias.CopiaChave',
        verbose_name='Copia da chave',
        on_delete=models.PROTECT,
        related_name='emprestimos',
        help_text='Copia de chave emprestada',
    )
    reserva = models.OneToOneField(
        'reservas.Reserva',
        verbose_name='Reserva',
        on_delete=models.SET_NULL,
        related_name='emprestimo',
        null=True,
        blank=True,
        help_text='Reserva que originou o emprestimo',
    )
    data_retirada = models.DateField('Data de retirada', help_text='Data de retirada da chave')
    data_prevista = models.DateField('Data prevista', help_text='Data prevista de devolucao')
    data_devolucao = models.DateField(
        'Data de devolucao',
        null=True,
        blank=True,
        help_text='Data efetiva de devolucao',
    )
    status = models.CharField(
        'Status',
        max_length=15,
        choices=StatusEmprestimo.choices,
        help_text='Status do emprestimo',
    )

    class Meta:
        verbose_name = 'Emprestimo'
        verbose_name_plural = 'Emprestimos'
        ordering = [Upper('usuario__nome')]

    def clean(self):
        super().clean()

        if not self.copia_chave_id:
            return

        chave = self.copia_chave.chave
        sala = chave.sala
        if not sala or not sala.eh_exclusiva:
            return

        if self.status not in {self.StatusEmprestimo.ABERTO, self.StatusEmprestimo.ATRASADO}:
            return

        conflito = Emprestimo.objects.filter(
            copia_chave__chave__sala_id=sala.id,
            status__in=[self.StatusEmprestimo.ABERTO, self.StatusEmprestimo.ATRASADO],
        )
        if self.pk:
            conflito = conflito.exclude(pk=self.pk)

        if conflito.exists():
            raise ValidationError(
                {
                    'copia_chave': (
                        'Sala exclusiva permite apenas um emprestimo aberto/atrasado por vez.'
                    )
                }
            )

    def __str__(self):
        return f"Emprestimo {self.id} - {self.get_status_display()}"
