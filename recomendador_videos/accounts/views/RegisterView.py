from django.shortcuts import render
from django.views import View
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.tokens import default_token_generator
from ..forms import CustomUserCreationForm
from ..models import UserProfile

class RegisterView(View):
    """
    View para registrar um novo usuário e enviar um e-mail de ativação.
    O usuário é criado como inativo e só poderá acessar a conta após confirmar o e-mail de ativação.
    Returns:
        HttpResponse: Página de registro ou confirmação pendente.
    """
    def get(self, request):
        """
        Exibe o formulário de criação de conta.
        Args:
            request (HttpRequest): A requisição HTTP recebida.
        Returns:
            HttpResponse: Página de registro renderizada com o formulário vazio.
        """
        form = CustomUserCreationForm()
        return render(request, 'apps/account/register.html', {'form': form})

    def post(self, request):
        """
        Processa o formulário de registro e cria a conta do usuário.
        Se o formulário for válido, cria o usuário, o define como inativo e envia o e-mail de ativação.
        Args:
            request (HttpRequest): A requisição HTTP com os dados do formulário.
        Returns:
            HttpResponse: Página de confirmação de ativação ou página de registro com erros.
        """
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Define como inativo até o email ser confirmado
            user.save()  # Apenas salva o usuário, o signal criará o perfil automaticamente

            avatar = form.cleaned_data.get('avatar')
            if avatar:
                profile = UserProfile.objects.get(user=user)
                profile.avatar = avatar
                profile.save()
                
            self.send_activation_email(user, request)

            return render(request, 'apps/account/activation_pending.html')

        return render(request, 'apps/account/register.html', {'form': form})

    def send_activation_email(self, user, request):
        """
        Gera e envia o e-mail de ativação com link de confirmação.
        Cria um token de ativação, monta a URL de ativação e envia o e-mail para o usuário.
        Args:
            user (User): O usuário recém-criado.
            request (HttpRequest): A requisição HTTP para capturar o domínio do site.
        """
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        domain = get_current_site(request).domain
        link = reverse('activate', kwargs={'uidb64': uid, 'token': token})
        activation_url = f"http://{domain}{link}"

        subject = "Confirme seu e-mail"
        from_email = "noreply@seudominio.com"
        to_email = [user.email]

        context = {'activation_url': activation_url}
        html_content = render_to_string('apps/account/email_confirmation.html', context)
        text_content = f"Olá,\n\nClique no link para ativar sua conta: {activation_url}\n\nSe você não se cadastrou, ignore este e-mail."

        email = EmailMultiAlternatives(subject, text_content, from_email, to_email)
        email.attach_alternative(html_content, "text/html")
        email.send()
