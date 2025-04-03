import random
import factory
import factory.fuzzy
from django.utils.timezone import now
from .models import Video, YouTubeCategory

# Dicionário de palavras para gerar títulos realistas
WORDS = [
    "python", "java", "c++", "C#", "javascript", "php","django", "dotenv", "laravel", 
    "aprender", "curso", "iniciante", "avançado", "tutorial", "programação", "desenvolvimento",
    "sintaxe", "exemplo", "introdução", "conceitos", "prático", "fácil", "rapido", "curiosidades",
    "engenharia", "software", "sistema", "logica", "matematica", "IA"
]

def generate_title():
    """
    Gera um título combinando de 3 a 6 palavras escolhidas aleatoriamente do dicionário.
    """
    num_palavras = random.randint(3, 6)
    # random.sample garante que as palavras não se repitam
    title = " ".join(random.sample(WORDS, num_palavras))
    return title.capitalize()

class VideoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Video
        django_get_or_create = ('youtube_id',)
    
    youtube_id = factory.Sequence(lambda n: f"yt_id_{n}")
    title = factory.LazyFunction(generate_title)
    description = factory.Faker('paragraph')
    thumbnail_url = factory.Faker('url')
    video_url = factory.Faker('url')
    view_count = factory.fuzzy.FuzzyInteger(0, 1000)
    like_count = factory.fuzzy.FuzzyInteger(0, 500)
    dislike_count = factory.fuzzy.FuzzyInteger(0, 50)
    duration = factory.fuzzy.FuzzyInteger(30, 600)
    category = "Unknown"
    language = "pt"
    channel_title = factory.Faker('company')
    channel_id = factory.Sequence(lambda n: f"channel_{n}")
    playlist_id = None
    playlist_title = None
    published_at = factory.LazyFunction(now)
    created_at = factory.LazyFunction(now)

class YouTubeCategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = YouTubeCategory
        django_get_or_create = ('category_id',)
    
    category_id = factory.Sequence(lambda n: f"cat_{n}")
    name = factory.Faker('word')
