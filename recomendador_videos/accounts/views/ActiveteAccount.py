from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.views import View

class ActivateAccountView(View):
     """
    View para ativação de conta de usuário, após receber o email 
    de ativaçao o usuario acessa a pagina de ativaçao pelo link.
    Args:
        request (HttpRequest): Requisição HTTP recebida.
        uidb64 (str): ID do usuário codificado.
        token (str): Token de ativação.
    Returns:
        HttpResponse: Página de sucesso ou erro de ativação.
    """
     def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return render(request, 'apps/account/activation_success.html')
        else:
            return render(request, 'apps/account/activation_invalid.html') 
