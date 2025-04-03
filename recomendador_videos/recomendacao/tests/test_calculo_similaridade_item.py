import logging
import pandas as pd
from django.test import TestCase
from recomendador_videos.youtube_integration.factories import VideoFactory

# Importa a função a ser testada
from recomendador_videos.recomendacao.services.similaridade import calcular_similaridade_itens

logging.basicConfig(
    filename="test_calculo_similaridade_itens_results.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)

class CalculoSimilaridadeItensTestCase(TestCase):
    def setUp(self):
        """
        Configuração inicial dos dados de teste:
        - Cria um vídeo alvo com conteúdo voltado para Python.
        - Cria uma lista de vídeos, dos quais alguns têm conteúdo semelhante e outros, diferente.
        """
        self.video_alvo = VideoFactory(
            title="Curso de Python para iniciantes",
            description="Aprenda Python do zero com exemplos práticos."
        )
        # Vídeos com conteúdo semelhante (relacionados a Python)
        self.video_similar1 = VideoFactory(
            title="Introdução ao Python",
            description="Aprenda os conceitos básicos de Python e comece a programar."
        )
        self.video_similar2 = VideoFactory(
            title="Tutorial Python",
            description="Curso rápido de Python com dicas e truques."
        )
        # Vídeos com conteúdo diferente (outras linguagens)
        self.video_diferente1 = VideoFactory(
            title="Curso de Java",
            description="Aprenda Java do zero e domine a programação orientada a objetos."
        )
        self.video_diferente2 = VideoFactory(
            title="Introdução a C++",
            description="Conceitos básicos de C++ para iniciantes."
        )
        # Lista de vídeos para comparação
        self.lista_videos = [
            self.video_similar1,
            self.video_similar2,
            self.video_diferente1,
            self.video_diferente2
        ]
        
        # Log dos dados de teste
        logging.info(f"Vídeo Alvo: {self.video_alvo.title} - {self.video_alvo.description}")
        for video in self.lista_videos:
            logging.info(f"Vídeo Comparado: {video.title} - {video.description}")
    
    def test_similaridade_itens(self):
        """
        Testa a similaridade de itens utilizando TF-IDF e similaridade do cosseno.
        Registra em log uma tabela com os vídeos retornados.
        """
        # Executa a função que calcula a similaridade entre o vídeo alvo e a lista de vídeos
        resultado = calcular_similaridade_itens(self.video_alvo, self.lista_videos, top_n=3)
        
        # Verifica se o resultado é uma lista
        self.assertIsInstance(resultado, list)
        
        # Log e criação da tabela: exibindo o ID e o título dos vídeos retornados
        if resultado:
            tabela = pd.DataFrame({
                "ID Vídeo": [video.id for video in resultado],
                "Título": [video.title for video in resultado]
            })
            log_tabela = tabela.to_string(index=False)
            logging.info(f"\nTabela de Vídeos Similares:\n{log_tabela}")
        else:
            logging.warning("Nenhum vídeo similar encontrado.")
        
        # Validação: pelo menos um dos vídeos retornados deve ter "Python" no título
        self.assertTrue(any("Python" in video.title for video in resultado),
                        "Nenhum vídeo relacionado a Python foi retornado como similar.")
