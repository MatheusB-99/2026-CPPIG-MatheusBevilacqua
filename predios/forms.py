from django import forms

from .models import Predio


class PredioForm(forms.ModelForm):
    class Meta:
        model = Predio
        fields = '__all__'
        error_messages = {
            'endereco': {'required': 'O endereco do predio e um campo obrigatorio'},
        }