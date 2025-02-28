from django.core.management.base import BaseCommand
from recomendador_videos.youtube_integration.services.search_service import busca_YT
from recomendador_videos.accounts.models import Interest

class Command(BaseCommand):
    """
    Preenche o banco de dados com vídeos buscados no YouTube com base nos termos informados.
    Se nenhum termo for passado, usa todos os interesses cadastrados no banco.
    """
    help = "Preenche o banco de dados com vídeos buscados no YouTube com base nos interesses ou termos informados."

    def add_arguments(self, parser):
        parser.add_argument(
            '--termos', 
            nargs='+', 
            type=str, 
            help='Lista de termos para buscar vídeos no YouTube'
        )
        parser.add_argument(
            '--arquivo', 
            type=str, 
            help='Caminho para um arquivo de texto com termos (um por linha)'
        )
        parser.add_argument(
            '--max_results', 
            type=int, 
            default=50, 
            help='Número máximo de vídeos a buscar por termo (padrão: 50)'
        )

    def handle(self, *args, **kwargs):
        termos = kwargs.get('termos')
        arquivo = kwargs.get('arquivo')
        max_results = kwargs.get('max_results')

        if not termos and not arquivo:
            self.stdout.write(self.style.WARNING("Nenhum termo fornecido, buscando por interesses cadastrados..."))
            termos = [interest.name for interest in Interest.objects.all()]

        if arquivo:
            try:
                with open(arquivo, 'r') as f:
                    termos = [linha.strip() for linha in f.readlines() if linha.strip()]
            except FileNotFoundError:
                self.stdout.write(self.style.ERROR(f"Arquivo '{arquivo}' não encontrado."))
                return

        if not termos:
            self.stdout.write(self.style.WARNING("Nenhum termo encontrado para buscar vídeos."))
            return

        self.stdout.write(f"Iniciando busca de vídeos para {len(termos)} termo(s)...")

        for termo in termos:
            try:
                self.stdout.write(f" Buscando vídeos para o termo: {termo}")
                videos = busca_YT(
                    termo, 
                    max_results
                )
                self.stdout.write(self.style.SUCCESS(f"{len(videos)} vídeos salvos no banco para o termo: {termo}"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Erro ao buscar vídeos para o termo '{termo}': {e}"))

        self.stdout.write(self.style.SUCCESS("Banco de dados preenchido com sucesso!"))
