from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from app.models import Evento, Participante, Organizador


class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = ['titulo', 'data', 'local', 'descricao', 'capacidade_max', 'imagem_banner']
        labels = {
            'titulo' : 'Título',
            'data' : 'Data',
            'local' : 'Local',
            'descricao' : 'Descrição',
            'capacidade_max' : 'Capacidade Máxima',
            'imagem_banner': 'Banner'
        }
        widgets = {
            'data': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

GENERO = (
    ('M', 'Masculino'),
    ('F', 'Feminino'),
    ('O', 'Outro'),
    ('P', 'Prefiro não dizer')
)

class ParticipanteForm(forms.ModelForm):
    class Meta:
        model = Participante
        fields = ['nome', 'telefone', 'genero', 'cidade', 'cpf']
        labels = {
            'nome' : 'Nome',
            'telefone' : 'Telefone',
            'genero' : 'Gênero',
            'cidade' : 'Cidade',
            'cpf' : 'CPF',
        }

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class OrganizadorForm(forms.ModelForm):
    class Meta:
        model = Organizador
        fields = ['nome_organizador', 'telefone', 'genero', 'cidade', 'cnpj']
        labels = {
            'nome_organizador' : 'Nome',
            'telefone' : 'Telefone',
            'genero' : 'Gênero',
            'cidade' : 'Cidade',
            'cnpj' : 'CNPJ',
        }


class ParticipanteSignUpForm(UserCreationForm):
    nome = forms.CharField(max_length=100)
    telefone = forms.CharField(max_length=20)
    genero = forms.ChoiceField(choices=GENERO)
    cidade = forms.CharField(max_length=100)
    cpf = forms.CharField(max_length=14)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class OrganizadorSignUpForm(UserCreationForm):
    nome_organizador = forms.CharField(max_length=100)
    telefone = forms.CharField(max_length=20)
    genero = forms.ChoiceField(choices=GENERO)
    cidade = forms.CharField(max_length=100)
    cnpj = forms.CharField(max_length=18)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']