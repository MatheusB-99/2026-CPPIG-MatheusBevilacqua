from django import forms

from .models import Chave


class ChaveForm(forms.ModelForm):
    class Meta:
        model = Chave
        fields = '__all__'
        error_messages = {
            'sala': {'required': 'A sala da chave e um campo obrigatorio'},
            'predio': {'required': 'O predio da chave e um campo obrigatorio'},
            'tipo': {'required': 'O tipo da chave e um campo obrigatorio'},
        }

    def clean(self):
        cleaned_data = super().clean()
        tipo = cleaned_data.get('tipo')
        sala = cleaned_data.get('sala')
        predio = cleaned_data.get('predio')

        if tipo == Chave.TipoChave.SALA and not sala:
            self.add_error('sala', 'Informe a sala para chave do tipo sala.')

        if tipo == Chave.TipoChave.SALA and predio:
            self.add_error('predio', 'Nao informe predio para chave do tipo sala.')

        if tipo == Chave.TipoChave.PREDIO and not predio:
            self.add_error('predio', 'Informe o predio para chave do tipo predio.')

        if tipo == Chave.TipoChave.PREDIO and sala:
            self.add_error('sala', 'Nao informe sala para chave do tipo predio.')

        return cleaned_data
