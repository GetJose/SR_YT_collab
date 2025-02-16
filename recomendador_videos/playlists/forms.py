from django import forms
from .models import Playlist, PlaylistVideo
from recomendador_videos.youtube_integration.models import Video

class PlaylistForm(forms.ModelForm):
    class Meta:
        model = Playlist
        fields = ['nome', 'descricao']

class PlaylistVideoForm(forms.ModelForm):
    video = forms.ModelChoiceField(
        queryset=Video.objects.all(),
        label="Escolha um vídeo",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = PlaylistVideo
        fields = ['video']
