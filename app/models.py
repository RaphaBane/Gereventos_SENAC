from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User
from django.db import models

GENERO = (
    ('M', 'Masculino'),
    ('F', 'Feminino'),
    ('O', 'Outro'),
    ('P', 'Prefiro não dizer')
)


class Participante(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    telefone = models.CharField(max_length=20)
    genero = models.CharField(max_length=10, choices=GENERO)
    cidade = models.CharField(max_length=100)
    cpf = models.CharField(max_length=14)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class Organizador(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nome_organizador = models.CharField(max_length=200)
    telefone = models.CharField(max_length=20)
    genero = models.CharField(max_length=10, choices=GENERO)
    cidade = models.CharField(max_length=100)
    cnpj = models.CharField(max_length=18)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome_organizador

class Evento(models.Model):
    organizador = models.ForeignKey(Organizador, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=100)
    descricao = models.TextField()
    data = models.DateTimeField()
    local = models.CharField(max_length=100)
    capacidade_max = models.IntegerField()
    imagem_banner = CloudinaryField(folder='media/banners')
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.titulo} - {self.local}'

class Inscricao(models.Model):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    participante = models.ForeignKey(Participante, on_delete=models.CASCADE)
    data_envio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.participante.nome} - {self.evento}'