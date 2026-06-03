from django import forms

from copias.models import CopiaChave
from .models import Reserva


class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = [
            'usuario',
            'copia_chave',
            'data_inicio',
            'horario_inicio',
            'data_fim',
            'horario_fim',
            'status',
        ]
        error_messages = {
            'usuario': {'required': 'O usuario da reserva e um campo obrigatorio'},
            'copia_chave': {'required': 'A copia da chave e um campo obrigatorio'},
            'data_inicio': {'required': 'A data de início da reserva e um campo obrigatorio'},
            'horario_inicio': {'required': 'O horario de início da reserva e um campo obrigatorio'},
            'data_fim': {'required': 'A data de término da reserva e um campo obrigatorio'},
            'horario_fim': {'required': 'O horario de término da reserva e um campo obrigatorio'},
            'status': {'required': 'O status da reserva e um campo obrigatorio'},
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['copia_chave'].queryset = CopiaChave.objects.filter(chave__tipo='sala')

    def clean(self):
        cleaned_data = super().clean()
        data_inicio = cleaned_data.get('data_inicio')
        horario_inicio = cleaned_data.get('horario_inicio')
        data_fim = cleaned_data.get('data_fim')
        horario_fim = cleaned_data.get('horario_fim')

        if not data_inicio or not horario_inicio or not data_fim or not horario_fim:
            raise forms.ValidationError('Os campos de início e término da reserva são obrigatórios.')

        if data_inicio > data_fim or (data_inicio == data_fim and horario_inicio >= horario_fim):
            raise forms.ValidationError('A data e horário de término devem ser posteriores ao início.')

        return cleaned_data

    def clean_copia_chave(self):
        copia_chave = self.cleaned_data.get('copia_chave')
        if copia_chave and copia_chave.chave.tipo == 'predio':
            raise forms.ValidationError('Chave de predio nao pode ser reservada.')
        return copia_chave
