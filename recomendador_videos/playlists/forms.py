from django import forms
from .models import Playlist, PlaylistVideo
from recomendador_videos.youtube_integration.models import Video

class PlaylistForm(forms.ModelForm):
    videos = forms.ModelMultipleChoiceField(
        queryset=Video.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Selecione os vídeos"
    )

    class Meta:
        model = Playlist
        fields = ['nome', 'descricao', 'videos']

class PlaylistVideoForm(forms.ModelForm):
    video = forms.ModelChoiceField(
        queryset=Video.objects.all(),
        label="Escolha um vídeo",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = PlaylistVideo
        fields = ['video']
