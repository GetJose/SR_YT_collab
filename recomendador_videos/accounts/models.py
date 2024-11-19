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
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    interests = models.ManyToManyField(Interest, blank=True)
    duracao_maxima = models.IntegerField(null=True, blank=True)  # Em minutos
    linguagens_preferidas = models.CharField(max_length=200, null=True, blank=True)  # Exemplo: 'pt,en'

    aplicar_filtros = models.BooleanField(default=True)  # Novo campo para ativar ou desativar filtros

    def __str__(self):
        return self.user.username
