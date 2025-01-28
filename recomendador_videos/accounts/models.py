from django.db import models
from django.contrib.auth.models import User

class Interest(models.Model):
    name = models.CharField(max_length=100, unique=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='sub_interests')

    def __str__(self):
        return self.name

    def is_root(self):
        return self.parent is None

class UserProfile(models.Model):
    DURATION_CHOICES = [
        ('short', 'Curtos (até 2 minutos)'),
        ('medium', 'Normais (até 15 minutos)'),
        ('long', 'Longos (mais de 15 minutos)'),
        ('none', 'Sem limite de tempo'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    interests = models.ManyToManyField(Interest, blank=True)
    duracao_faixa = models.CharField(max_length=10, choices=DURATION_CHOICES, null=True, blank=True)  
    linguagens_preferidas = models.CharField(max_length=200, null=True, blank=True) 
    aplicar_filtros = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username