from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import UserProfile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Cria automaticamente um perfil para o usuário recém-registrado.
    Este sinal é acionado após a criação de um novo usuário, 
    garantindo que cada usuário tenha um perfil associado.
    Args:
        sender (Model): O modelo que enviou o sinal (User).
        instance (User): A instância do usuário recém-criado.
        created (bool): Indica se o usuário foi criado (True) ou atualizado (False).
        **kwargs: Parâmetros adicionais do sinal.
    """
    if created:
        UserProfile.objects.create(user=instance)
