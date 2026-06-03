from django import forms

from .models import Sala


class SalaForm(forms.ModelForm):
    tipo_sala = forms.ChoiceField(
        label='Tipo da sala',
        choices=Sala.TipoSala.choices,
    )

    class Meta:
        model = Sala
        fields = ['predio']
        error_messages = {
            'predio': {'required': 'O predio da sala e um campo obrigatorio'},
            'tipo_sala': {'required': 'O tipo da sala e um campo obrigatorio'},
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk and self.instance.tipo_sala:
            self.fields['tipo_sala'].initial = self.instance.tipo_sala

    def clean_tipo_sala(self):
        tipo_sala = self.cleaned_data.get('tipo_sala')
        if not tipo_sala:
            raise forms.ValidationError('O tipo da sala e um campo obrigatorio.')
        return tipo_sala