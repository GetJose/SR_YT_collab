from django import forms
from .models import UserProfile, Interest
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].help_text = None
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None

        self.fields['username'].widget.attrs.update({
            'placeholder': 'Nome de usuário'
        })
        self.fields['password1'].widget.attrs.update({
            'placeholder': 'Senha'
        })
        self.fields['password2'].widget.attrs.update({
            'placeholder': 'Confirme a senha'
        })

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
        # Carrega os interesses existentes do usuário para serem exibidos como selecionados
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
        # Salvar as linguagens como string separada por vírgula ou string vazia
        profile.linguagens_preferidas = ','.join(linguagens) if linguagens else ''
        if commit:
            profile.save()
        return profile