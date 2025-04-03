import factory
import factory.fuzzy
from django.contrib.auth.models import User
from .models import UserProfile

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ('username',)
    
    username = factory.Sequence(lambda n: f"usuario{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@exemplo.com")
    password = factory.PostGenerationMethodCall('set_password', 'senha123')

class UserProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserProfile
    
    user = factory.SubFactory(UserFactory)
    duracao_faixa = 'none'
    linguagens_preferidas = 'pt'
    aplicar_filtros = True
    role = 'student'
