import factory
import factory.fuzzy
from django.utils.timezone import now
from .models import VideoInteraction, UserSimilarity
from recomendador_videos.accounts.factories import UserFactory
from recomendador_videos.youtube_integration.factories import VideoFactory


class VideoInteractionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = VideoInteraction
        django_get_or_create = ('user', 'video')
    
    user = factory.SubFactory(UserFactory)
    video = factory.SubFactory(VideoFactory)
    rating = factory.fuzzy.FuzzyChoice([1, -1])
    method = factory.fuzzy.FuzzyChoice(["user_based", "item_based", "hybrid"])

class UserSimilarityFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserSimilarity
    
    user = factory.SubFactory(UserFactory)
    similar_user = factory.SubFactory(UserFactory)
    score = factory.fuzzy.FuzzyFloat(0.0, 1.0)