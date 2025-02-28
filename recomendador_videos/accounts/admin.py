from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import UserProfile, Interest

class UserProfileInline(admin.StackedInline):
    """
    Configuração para exibir o perfil do usuário no painel de administração.
    Usa uma interface empilhada para exibir os campos do perfil, incluindo os interesses.
    Atributos:
        model (UserProfile): Modelo de perfil do usuário.
        can_delete (bool): Define se o perfil pode ser excluído (False para evitar remoção acidental).
        verbose_name_plural (str): Nome plural exibido no admin.
        filter_horizontal (tuple): Configuração para exibir os interesses com seleção múltipla.
    Métodos:
        get_readonly_fields: Define os campos somente leitura com base no tipo de usuário.
    """
    model = UserProfile
    can_delete = False
    verbose_name_plural = "Perfil do Usuário"
    filter_horizontal = ('interests',)

    def get_readonly_fields(self, request, obj=None):
        """
        Define os campos somente leitura com base no tipo de usuário.
        Args:
            request (HttpRequest): A requisição HTTP do admin.
            obj (User, opcional): O objeto de usuário sendo editado.
        Returns:
            list: Lista de campos somente leitura.
        """
        if not request.user.is_superuser:
            return ['role']  # Somente administradores podem editar o campo
        return []

class CustomUserAdmin(UserAdmin):
    """
    Configuração personalizada do admin para o modelo User.
    Adiciona a exibição do perfil do usuário como um inline dentro da interface de usuário do admin.
    Atributos:
        inlines (tuple): Define os inlines para exibir informações relacionadas ao usuário.
    """
    inlines = (UserProfileInline,)

# Desregistrar o admin padrão e registrar a configuração personalizada
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Interest)
