from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.contrib.auth import authenticate
from django.shortcuts import redirect

class CustomLoginView(LoginView):
    """
    View personalizada para exibir a página de login e processar as credenciais do usuário.
    Se o usuário já estiver autenticado, é redirecionado para a página inicial.  
    Em caso de falha no login, exibe mensagens de erro específicas.
    """
    def dispatch(self, request, *args, **kwargs):
        """
        Verifica se o usuário já está autenticado.
        Args:
            request (HttpRequest): A requisição HTTP recebida.
            *args: Argumentos posicionais adicionais.
            **kwargs: Argumentos nomeados adicionais.
        Returns:
            HttpResponseRedirect: Redireciona para a home se o usuário estiver logado.
            HttpResponse: Página de login se o usuário não estiver autenticado.
        """
        if request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def form_invalid(self, form):
        """
        Trata o caso de credenciais inválidas no login.
        Se o usuário existir mas estiver inativo, exibe uma mensagem informando que a conta está inativa.
        Caso contrário, exibe uma mensagem de erro padrão.
        Args:
            form (AuthenticationForm): Formulário de autenticação inválido.
        Returns:
            HttpResponse: Página de login com mensagens de erro.
        """
        username = self.request.POST.get('username')
        password = self.request.POST.get('password')

        user = authenticate(self.request, username=username, password=password)

        if user and not user.is_active:
            messages.error(self.request, "Conta ainda inativa. Verifique seu e-mail para ativá-la.")
        else:
            messages.error(self.request, "Nome de usuário ou senha incorretos.")

        return super().form_invalid(form)
