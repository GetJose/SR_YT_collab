from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from .models import UserProfile, Interest

class CustomPasswordChangeForm(PasswordChangeForm):
    """
    Formulário personalizado para alteração de senha.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        fields_attrs = {
            'old_password': 'Senha atual',
            'new_password1': 'Nova senha',
            'new_password2': 'Confirme a nova senha'
        }
        
        for field, placeholder in fields_attrs.items():
            self.fields[field].widget.attrs.update({'class': 'form-control', 'placeholder': placeholder})


class CustomUserCreationForm(UserCreationForm):
    """
    Formulário personalizado para criação de usuário.
    """
    email = forms.EmailField(required=True, label="Email")
    avatar = forms.ImageField(required=False, label="Avatar")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'avatar']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            'username': 'Nome de usuário',
            'email': 'Email',
            'password1': 'Senha',
            'password2': 'Confirme a senha'
        }
        
        for field, placeholder in placeholders.items():
            self.fields[field].widget.attrs.update({'placeholder': placeholder})
            self.fields[field].help_text = None

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este email já está em uso. Tente outro.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.is_active = False
        
        if commit:
            user.save()
            UserProfile.objects.create(
                user=user, 
                avatar=self.cleaned_data.get('avatar', 'avatars/default.png')
            )
        return user


class UserEditForm(UserChangeForm):
    """
    Formulário para editar dados básicos do usuário.
    """
    password = None
    first_name = forms.CharField(required=True, label="Nome")
    last_name = forms.CharField(required=True, label="Sobrenome")
    email = forms.EmailField(required=True, label="Email")

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class UserProfileEditForm(forms.ModelForm):
    """
    Formulário para editar o perfil do usuário.
    """
    first_name = forms.CharField(max_length=150, required=True, label="Nome")
    last_name = forms.CharField(max_length=150, required=True, label="Sobrenome")
    email = forms.EmailField(required=True, label="Email")
    role = forms.ChoiceField(choices=UserProfile.ROLE_CHOICES, required=True, label="Função")
    avatar = forms.ImageField(
        required=False,
        label="Alterar avatar",
        widget=forms.ClearableFileInput(attrs={'aria-label': 'Modificar imagem de perfil'})
    )

    class Meta:
        model = UserProfile
        fields = ['avatar', 'role']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if self.instance and self.instance.user:
            self._prepopulate_user_fields()

        if user and not user.is_superuser:
            self.fields.pop('role')

    def _prepopulate_user_fields(self):
        """Preenche campos com dados do usuário."""
        self.fields['first_name'].initial = self.instance.user.first_name
        self.fields['last_name'].initial = self.instance.user.last_name
        self.fields['email'].initial = self.instance.user.email

    def save(self, commit=True):
        user_profile = super().save(commit=False)
        user = user_profile.user
        
        self._update_user_fields(user)
        
        if commit:
            user.save()
            user_profile.save()
        return user_profile

    def _update_user_fields(self, user):
        """Atualiza campos do usuário."""
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']


class InterestForm(forms.ModelForm):
    """
    Formulário para seleção de áreas de interesse.
    """
    interests = forms.ModelMultipleChoiceField(
        queryset=Interest.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = UserProfile
        fields = ['interests']

    def clean_interests(self):
        return self.cleaned_data.get('interests')

    def save(self, commit=True):
        profile = super().save(commit=False)
        profile.interests.set(self.cleaned_data.get('interests', []))
        if commit:
            profile.save()
        return profile


class UserProfileFilterForm(forms.ModelForm):
    """
    Formulário para filtrar vídeos com base na duração e linguagem.
    """
    DURATION_CHOICES = [
        ('short', 'Curtos (até 2 minutos)'),
        ('medium', 'Normais (até 15 minutos)'),
        ('long', 'Longos (mais de 15 minutos)'),
        ('none', 'Sem limite de tempo'),
    ]

    duracao_faixa = forms.ChoiceField(
        required=False,
        choices=DURATION_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Faixa de Duração"
    )

    linguagens_preferidas = forms.MultipleChoiceField(
        required=False,
        choices=[('pt', 'Português'), ('en', 'Inglês'), ('es', 'Espanhol')],
        widget=forms.CheckboxSelectMultiple(),
        label="Linguagens Preferidas"
    )

    aplicar_filtros = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(),
        label='Aplicar filtros nas buscas de vídeos'
    )

    class Meta:
        model = UserProfile
        fields = ['duracao_faixa', 'linguagens_preferidas', 'aplicar_filtros']

    def save(self, commit=True):
        profile = super().save(commit=False)
        linguagens = self.cleaned_data.get('linguagens_preferidas', [])
        profile.linguagens_preferidas = ','.join(linguagens) if linguagens else ''
        if commit:
            profile.save()
        return profile
