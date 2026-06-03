from django import forms

from copias.models import CopiaChave
from .models import Emprestimo


class EmprestimoForm(forms.ModelForm):
    class Meta:
        model = Emprestimo
        fields = '__all__'
        error_messages = {
            'usuario': {'required': 'O usuario do emprestimo e um campo obrigatorio'},
            'copia_chave': {'required': 'A copia da chave e um campo obrigatorio'},
            'reserva': {'required': 'A reserva do emprestimo e um campo obrigatorio'},
            'data_retirada': {'required': 'A data de retirada e um campo obrigatorio'},
            'data_prevista': {'required': 'A data prevista e um campo obrigatorio'},
            'data_devolucao': {'required': 'A data de devolucao e um campo obrigatorio'},
            'status': {'required': 'O status do emprestimo e um campo obrigatorio'},
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['copia_chave'].queryset = CopiaChave.objects.filter(chave__tipo='sala')

    def clean_copia_chave(self):
        copia_chave = self.cleaned_data.get('copia_chave')
        if copia_chave and copia_chave.chave.tipo == 'predio':
            raise forms.ValidationError('Chave de predio nao pode ser emprestada.')
        return copia_chave
