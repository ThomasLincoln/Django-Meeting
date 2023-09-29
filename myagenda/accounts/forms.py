from django import forms
from django.contrib.auth.models import User
from .models import Compromisso

class CompromissoForm(forms.ModelForm):
    class Meta:
        model = Compromisso
        exclude = ['criador']  # Exclua o campo 'criador' do formulário

    participantes = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True 
    )