from django.core.management.base import BaseCommand
from recomendador_videos.youtube_integration.models import YouTubeCategory
from recomendador_videos.youtube_integration.services.yt_services import get_youtube_client


class Command(BaseCommand):
    help = "Popula o banco de dados com as categorias do YouTube usando a API do YouTube."

    def handle(self, *args, **kwargs):
        try:
            youtube = get_youtube_client()
        except ValueError as e:
            self.stdout.write(self.style.ERROR(str(e)))
            return

        request = youtube.videoCategories().list(
            part="snippet",
            regionCode="BR"  # Pode ser alterado conforme necessário
        )
        response = request.execute()

        if "items" in response:
            for item in response["items"]:
                category_id = item["id"]
                category_name = item["snippet"]["title"]

                YouTubeCategory.objects.update_or_create(
                    category_id=category_id,
                    defaults={"name": category_name}
                )

                self.stdout.write(self.style.SUCCESS(f"Categoria '{category_name}' ({category_id}) salva!"))
        else:
            self.stdout.write(self.style.ERROR("Nenhuma categoria encontrada!"))
