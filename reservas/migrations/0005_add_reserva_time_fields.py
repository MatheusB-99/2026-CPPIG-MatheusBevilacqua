from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservas', '0004_drop_notificacoes_table'),
    ]

    operations = [
        migrations.AddField(
            model_name='reserva',
            name='data_inicio',
            field=models.DateField(blank=True, help_text='Data de início da reserva', null=True, verbose_name='Data de início'),
        ),
        migrations.AddField(
            model_name='reserva',
            name='data_fim',
            field=models.DateField(blank=True, help_text='Data de término da reserva', null=True, verbose_name='Data de término'),
        ),
        migrations.AddField(
            model_name='reserva',
            name='horario_fim',
            field=models.TimeField(blank=True, help_text='Horário de término da reserva', null=True, verbose_name='Horário de término'),
        ),
        migrations.AddField(
            model_name='reserva',
            name='horario_inicio',
            field=models.TimeField(blank=True, help_text='Horário de início da reserva', null=True, verbose_name='Horário de início'),
        ),
        migrations.AlterField(
            model_name='reserva',
            name='data',
            field=models.DateField(blank=True, help_text='Data da reserva', null=True, verbose_name='Data'),
        ),
        migrations.AlterField(
            model_name='reserva',
            name='horario',
            field=models.TimeField(blank=True, help_text='Horario da reserva', null=True, verbose_name='Horario'),
        ),
    ]
