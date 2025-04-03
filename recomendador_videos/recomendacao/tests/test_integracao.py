import logging
from django.test import TestCase
from recomendador_videos.accounts.factories import UserFactory
from recomendador_videos.youtube_integration.factories import VideoFactory
from recomendador_videos.youtube_integration.models import Video
from recomendador_videos.recomendacao.models import VideoInteraction
from recomendador_videos.recomendacao.services.recomendacao import recomendar_videos_user_based
from recomendador_videos.recomendacao.services.avaliar import avaliar_video, obter_avaliacoes_do_usuario
from recomendador_videos.youtube_integration.services.search_service import busca_YT  

# Configuração do logging
logging.basicConfig(
    filename="test_integracao_recomendacao.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)

class IntegracaoRecomendacaoTestCase(TestCase):
    def setUp(self):
        """Configuração inicial: Criação de usuários e pesquisa de vídeos no YouTube."""
        self.user1 = UserFactory(username="usuario1")
        self.user2 = UserFactory(username="usuario2")

        self.temas_pesquisa = ["Python code", "Framework Django"]
        self.videos = []

        # Simula pesquisa no YouTube e salva os vídeos no banco de dados
        for tema in self.temas_pesquisa:
            resultados = busca_YT(tema)  
            for video_data in resultados:
                video, _ = Video.objects.get_or_create(
                    youtube_id=video_data.youtube_id,  
                    defaults={"title": video_data.title}
                )
                self.videos.append(video)

        logging.info(f"{len(self.videos)} vídeos carregados no banco de dados.")

    def test_fluxo_completo_recomendacao(self):
        """Testa a recomendação desde a pesquisa até a geração da lista final."""

        # Usuário 1 e 2 avaliam vídeos
        self.realizar_avaliacoes(self.user1, user_index=0)
        self.realizar_avaliacoes(self.user2, user_index=1)

        # Obter avaliações para logs
        avaliacoes_user1 = obter_avaliacoes_do_usuario(self.user1, self.videos)
        avaliacoes_user2 = obter_avaliacoes_do_usuario(self.user2, self.videos)

        # Log das avaliações
        logging.info(f"Avaliações do {self.user1.username}: {avaliacoes_user1}")
        logging.info(f"Avaliações do {self.user2.username}: {avaliacoes_user2}")

        # Gera recomendações para o usuário 1
        recomendacoes = recomendar_videos_user_based(self.user1, metodo_similaridade="cosseno")

        # Log das recomendações geradas
        logging.info(f"Recomendações para {self.user1.username}: {[video.youtube_id for video in recomendacoes]}")

        # Verificações do teste
        self.assertIsNotNone(recomendacoes, "A recomendação retornou None.")
        self.assertGreater(len(recomendacoes), 0, "Nenhuma recomendação foi gerada.")
    
    def realizar_avaliacoes(self, user, user_index, videos_comuns=25, exclusivos_positivo=15, exclusivos_negativo=10):
        """Avalia vídeos garantindo alguns vídeos comuns e outros exclusivos para cada usuário."""
        
        # Escolher vídeos comuns para ambos os usuários
        videos_comuns_lista = self.videos[:videos_comuns]
        # Escolher vídeos exclusivos para cada usuário
        inicio_exclusivo = videos_comuns + (exclusivos_positivo + exclusivos_negativo) * user_index
        fim_exclusivo = inicio_exclusivo + exclusivos_positivo + exclusivos_negativo
        videos_exclusivos_lista = self.videos[inicio_exclusivo:fim_exclusivo]

        # Avaliar vídeos comuns como positivos
        for video in videos_comuns_lista:
            _, msg = avaliar_video(video.youtube_id, user, 1, "teste_integracao")
            logging.info(f"{user.username} avaliou {video.title} como positivo.")

        # Avaliar parte dos vídeos exclusivos como positivos
        for video in videos_exclusivos_lista[:exclusivos_positivo]:
            _, msg = avaliar_video(video.youtube_id, user, 1, "teste_integracao")
            logging.info(f"{user.username} avaliou {video.title} como positivo.")

        # Avaliar o restante dos vídeos exclusivos como negativos
        for video in videos_exclusivos_lista[exclusivos_positivo:]:
            _, msg = avaliar_video(video.youtube_id, user, -1, "teste_integracao")
            logging.info(f"{user.username} avaliou {video.title} como negativo.")
