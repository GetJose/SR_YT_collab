from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import UserProfile, Interest
from django.contrib.auth.forms import PasswordChangeForm

class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Senha atual'})
        self.fields['new_password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Nova senha'})
        self.fields['new_password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirme a nova senha'})


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email")  # Adiciona o campo de email
    avatar = forms.ImageField(required=False, label="Avatar")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'avatar']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = None
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None

        self.fields['username'].widget.attrs.update({'placeholder': 'Nome de usuário'})
        self.fields['email'].widget.attrs.update({'placeholder': 'Email'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Senha'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Confirme a senha'})

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este email já está em uso. Tente outro.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.is_active = False  # Define usuário como inativo até confirmação por email
        if commit:
            user.save()
            UserProfile.objects.create(user=user, avatar=self.cleaned_data.get('avatar', 'avatars/default.png'))
        return user
    
class UserEditForm(UserChangeForm):
    password = None  # Remove o campo de senha do formulário
    first_name = forms.CharField(required=True, label="Nome")
    last_name = forms.CharField(required=True, label="Sobrenome")
    email = forms.EmailField(required=True, label="Email")

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class UserProfileEditForm(forms.ModelForm):
    first_name = forms.CharField(max_length=150, required=True, label="Nome")
    last_name = forms.CharField(max_length=150, required=True, label="Sobrenome")
    email = forms.EmailField(required=True, label="Email")
    role = forms.ChoiceField(
        choices=UserProfile.ROLE_CHOICES,
        required=True,
        label="Função"  
    )

    class Meta:
        model = UserProfile
        fields = ['avatar', 'role']  

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email

        if user and not user.is_superuser:
            del self.fields['role']


    def save(self, commit=True):
        user_profile = super().save(commit=False)
        user = user_profile.user
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if 'role' in self.cleaned_data and self.instance.user.is_superuser:
            user_profile.role = self.cleaned_data['role']

        if commit:
            user.save()
            user_profile.save()

        return user_profile

class InterestForm(forms.ModelForm):
    interests = forms.ModelMultipleChoiceField(
        queryset=Interest.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    
    new_interests = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Adicione novas áreas de interesse'}),
        required=False
    )

    class Meta:
        model = UserProfile
        fields = ['interests']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['interests'].initial = self.instance.interests.all()

    def clean_interests(self):
        interests = self.cleaned_data.get('interests')
        if len(interests) < 1:
            raise forms.ValidationError("Selecione pelo menos uma das áreas de interesse.")
        return interests

    def save(self, commit=True):
        profile = super().save(commit=False)
        interests = self.cleaned_data.get('interests')

        new_interests_text = self.cleaned_data.get('new_interests')
        if new_interests_text:
            new_interests_list = [i.strip() for i in new_interests_text.split(',')]
            for interest_name in new_interests_list:
                interest, created = Interest.objects.get_or_create(name=interest_name)
                interests = interests | Interest.objects.filter(id=interest.id)

        profile.interests.set(interests)

        if commit:
            profile.save()
        return profile
    
class UserProfileFilterForm(forms.ModelForm):
    DURATION_CHOICES = [
        ('short', 'Curtos (até 2 minutos)'),
        ('medium', 'Normais (até 15 minutos)'),
        ('long', 'Longos (mais de 15 minutos)'),
        ('none', 'Sem limite de tempo'),
    ]

    class Meta:
        model = UserProfile
        fields = ['duracao_faixa', 'linguagens_preferidas', 'aplicar_filtros']

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

    def save(self, commit=True):
        profile = super().save(commit=False)
        linguagens = self.cleaned_data.get('linguagens_preferidas', [])
        profile.linguagens_preferidas = ','.join(linguagens) if linguagens else ''
        if commit:
            profile.save()
        return profile
