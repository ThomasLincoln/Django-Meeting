# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Compromisso(models.Model):
    titulo = models.CharField(max_length=255)
    descricao = models.TextField(blank=True, null=True)
    data = models.DateField()
    hora = models.TimeField()
    local = models.CharField(max_length=255, blank=True, null=True)
    criador = models.ForeignKey(User, on_delete=models.CASCADE, related_name='compromissos_criados')
    participantes = models.ManyToManyField(User, blank=True)
    estado = models.CharField(max_length=20, choices=[('Agendado', 'Agendado'), ('Cancelado', 'Cancelado'), ('Concluído', 'Concluído')])

    class Meta: 
        ordering = ('data',)
        verbose_name_plural = 'Compromissos'
    def __str__(self):
        return self.titulo

