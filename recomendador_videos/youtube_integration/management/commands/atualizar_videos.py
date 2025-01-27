from django.core.management.base import BaseCommand
from googleapiclient.discovery import build
from ...models import Video, YouTubeCategory
from ...services import converter_duracao_iso_para_segundos, atualizar_categoria
import os
import isodate

class Command(BaseCommand):
    help = "Atualiza os vídeos no banco de dados com informações mais recentes da API do YouTube"

    def handle(self, *args, **kwargs):
        YOUTUBE_API_KEY = os.environ.get('YOUTUBE_API_KEY')
        if not YOUTUBE_API_KEY:
            self.stdout.write(self.style.ERROR("A chave da API do YouTube não está configurada."))
            return

        youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
        videos = Video.objects.all()
        
        self.stdout.write(f"Iniciando a atualização de {videos.count()} vídeos...")

        for video in videos:
            try:
                # Busca detalhes atualizados do vídeo
                video_details = youtube.videos().list(
                    part='contentDetails,statistics,snippet,status',
                    id=video.youtube_id
                ).execute()

                if not video_details['items']:
                    self.stdout.write(self.style.WARNING(f"Vídeo {video.youtube_id} não encontrado."))
                    continue

                details = video_details['items'][0]
                snippet = details['snippet']
                status = details.get('status', {})

                # Atualizando campos
                video.duration = converter_duracao_iso_para_segundos(details['contentDetails']['duration'])
                video.view_count = details['statistics'].get('viewCount', 0)
                video.like_count = details['statistics'].get('likeCount', 0)
                video.dislike_count = details['statistics'].get('dislikeCount', 0)
                video.language = status.get('defaultAudioLanguage', 'Unknown')
                video.channel_title = snippet.get('channelTitle', 'Unknown')
                video.category = atualizar_categoria(youtube, snippet.get('categoryId', 'Unknown'))
                video.save()

                self.stdout.write(self.style.SUCCESS(f"Vídeo {video.youtube_id} atualizado com sucesso."))

            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Erro ao atualizar o vídeo {video.youtube_id}: {e}"))

        self.stdout.write(self.style.SUCCESS("Atualização concluída!"))
