from django import forms

from .models import CopiaChave


class CopiaChaveForm(forms.ModelForm):
    class Meta:
        model = CopiaChave
        fields = '__all__'
        error_messages = {
            'chave': {'required': 'A chave da copia e um campo obrigatorio'},
            'status': {'required': 'O status da copia e um campo obrigatorio'},
            'emergencia': {'required': 'Informe se a copia e de emergencia'},
        }