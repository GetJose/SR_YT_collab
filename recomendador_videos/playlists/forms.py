from django import forms
from .models import Playlist, PlaylistVideo
from recomendador_videos.youtube_integration.models import Video

class PlaylistForm(forms.ModelForm):
    """
    Formulário para criação e edição de playlists.
    Permite ao usuário definir o nome, descrição, nível de acesso e selecionar vídeos para compor a playlist.
    Atributos:
        videos (ModelMultipleChoiceField): Campo para selecionar múltiplos vídeos.
        nivel_acesso (ChoiceField): Campo para definir o nível de acesso (pública ou privada).
    Meta:
        model (Playlist): Modelo da playlist.
        fields (list): Campos a serem exibidos no formulário.
    """
    videos = forms.ModelMultipleChoiceField(
        queryset=Video.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Selecione os vídeos"
    )
    nivel_acesso = forms.ChoiceField(
        choices=Playlist.NIVEIS_ACESSO,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Nível de Acesso"
    )
    class Meta:
        model = Playlist
        fields = ['nome', 'descricao', 'nivel_acesso', 'videos']
        
class PlaylistVideoForm(forms.ModelForm):
    """
    Formulário para adicionar vídeos a uma playlist existente.
    Atributos:
        video (ModelChoiceField): Campo para escolher um vídeo específico.
    Meta:
        model (PlaylistVideo): Modelo que relaciona playlist e vídeo.
        fields (list): Campos a serem exibidos no formulário.
    """
    video = forms.ModelChoiceField(
        queryset=Video.objects.all(),
        label="Escolha um vídeo",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    class Meta:
        model = PlaylistVideo
        fields = ['video']
