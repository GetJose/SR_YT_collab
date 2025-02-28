from django.core.management.base import BaseCommand
from django.utils.timezone import now, timedelta
from ...models import Video
from ...services.yt_services import get_youtube_client
from ...utils.banco import converter_duracao_iso_para_segundos, atualizar_categoria, buscar_e_atualizar_playlist

class Command(BaseCommand):
    """
    Comando para atualizar vídeos existentes no banco de dados com informações mais recentes da API do YouTube,
    incluindo as playlists. Permite filtrar por ID ou por data de criação.
    """
    help = "Atualiza vídeos no banco de dados com informações mais recentes da API do YouTube e busca playlists."

    def add_arguments(self, parser):
        parser.add_argument(
            '--video_ids',
            nargs='+',  
            type=str,
            help='ID(s) do vídeo no YouTube para atualizar. Se não informado, atualiza todos ou pelo prazo definido.'
        )
        parser.add_argument(
            '--days',
            type=int,
            help='Atualiza vídeos criados nos últimos X dias. Ignorado se IDs forem passados.'
        )

    def handle(self, *args, **kwargs):
        try:
            youtube = get_youtube_client()
            video_ids = kwargs.get('video_ids')
            days = kwargs.get('days')

            # Filtrar vídeos com base nos argumentos
            if video_ids:
                videos = Video.objects.filter(youtube_id__in=video_ids)
            elif days is not None:
                cutoff_date = now() - timedelta(days=days)
                videos = Video.objects.filter(published_at__gte=cutoff_date)
                self.stdout.write(f"Filtrando vídeos publicados nos últimos {days} dias...")
            else:
                videos = Video.objects.all()

            if not videos.exists():
                self.stdout.write(self.style.WARNING("Nenhum vídeo encontrado para atualizar."))
                return

            self.stdout.write(f"Iniciando a atualização de {videos.count()} vídeo(s)...")

            for video in videos:
                try:
                    # Buscar detalhes do vídeo
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

                    # Atualizar os campos do vídeo
                    video.title = snippet['title']
                    video.description = snippet['description']
                    video.thumbnail_url = snippet['thumbnails']['default']['url']
                    video.video_url = f"https://www.youtube.com/watch?v={video.youtube_id}"
                    video.duration = converter_duracao_iso_para_segundos(details['contentDetails']['duration'])
                    video.view_count = int(details['statistics'].get('viewCount', 0))
                    video.like_count = int(details['statistics'].get('likeCount', 0))
                    video.dislike_count = int(details['statistics'].get('dislikeCount', 0))
                    video.language = status.get('defaultAudioLanguage', 'unknown')
                    video.channel_title = snippet.get('channelTitle', 'unknown')
                    video.channel_id = snippet.get('channelId', None)
                    video.category = atualizar_categoria(youtube, snippet.get('categoryId', 'unknown'))
                    video.published_at = snippet.get('publishedAt')

                    video.save()
                    self.stdout.write(self.style.SUCCESS(f"✅ Vídeo {video.youtube_id} atualizado com sucesso."))

                    # Buscar e atualizar a playlist (opcional, se ainda não estiver salva)
                    if not video.playlist_id:
                        buscar_e_atualizar_playlist(video, youtube)

                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Erro ao atualizar o vídeo {video.youtube_id}: {e}"))

            self.stdout.write(self.style.SUCCESS("Atualização concluída!"))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Erro geral ao conectar com o YouTube ou buscar vídeos: {e}"))
