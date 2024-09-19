from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'recomendador_videos.accounts'

    def ready(self):
        import recomendador_videos.accounts.signals