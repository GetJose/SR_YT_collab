import os
import uuid
from django.db import models
from django.contrib.auth.models import User

def user_avatar_path(instance, filename):
    """Gera um nome único para o arquivo de avatar"""
    ext = filename.split('.')[-1]  # Obtém a extensão do arquivo original
    filename = f"{uuid.uuid4().hex}.{ext}"  # Gera um nome aleatório com a extensão original
    return os.path.join('avatars/', filename)


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
    ROLE_CHOICES = [
        ('student', 'Aluno'),
        ('teacher', 'Professor'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to=user_avatar_path, default='avatars/default.png', blank=True, null=True)
    interests = models.ManyToManyField(Interest, blank=True)
    duracao_faixa = models.CharField(max_length=10, choices=DURATION_CHOICES, default='none')  
    linguagens_preferidas = models.CharField(max_length=200, null=True, blank=True) 
    aplicar_filtros = models.BooleanField(default=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')

    def __str__(self):
        return self.user.username