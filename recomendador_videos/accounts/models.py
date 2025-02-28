import os
import uuid
from django.db import models
from django.contrib.auth.models import User

def user_avatar_path(instance, filename):
    """
    Gera um caminho único para salvar o avatar do usuário.
    O nome do arquivo é substituído por um UUID para evitar conflitos.
    Args:
        instance (UserProfile): Instância do perfil do usuário.
        filename (str): Nome original do arquivo enviado.
    Returns:
        str: Caminho para salvar o arquivo, ex: 'avatars/<uuid>.ext'.
    """
    ext = filename.split('.')[-1]  # Obtém a extensão do arquivo original
    filename = f"{uuid.uuid4().hex}.{ext}"  # Gera um nome aleatório com a extensão original
    return os.path.join('avatars/', filename)

class Interest(models.Model):
    """
    Modelo para representar áreas de interesse do usuário.
    Permite a criação de hierarquias com subinteresses.
    Atributos:
        name (str): Nome do interesse (único).
        parent (Interest): Interesse pai, para formar hierarquias (opcional).
    Métodos:
        __str__: Retorna o nome do interesse em formato de string.
        is_root: Verifica se o interesse é um nível raiz.
    """
    name = models.CharField(max_length=100, unique=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='sub_interests')

    def __str__(self):
        return self.name

    def is_root(self):
        return self.parent is None

class UserProfile(models.Model):
    """
    Modelo de perfil do usuário, estendido a partir do modelo de usuário padrão do Django.
    Armazena informações adicionais como avatar, interesses, filtros de conteúdo e função.
    Atributos:
        user (User): Usuário associado ao perfil.
        avatar (ImageField): Imagem de perfil do usuário.
        interests (ManyToManyField): Interesses selecionados pelo usuário.
        duracao_faixa (CharField): Faixa de duração preferida para vídeos.
        linguagens_preferidas (CharField): Idiomas preferidos do usuário.
        aplicar_filtros (BooleanField): Define se os filtros de busca serão aplicados.
        role (CharField): Função do usuário (aluno ou professor).
    Métodos:
        __str__: Retorna o nome de usuário associado ao perfil.
    """
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