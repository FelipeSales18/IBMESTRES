from django.apps import AppConfig

class PlayersappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'playersapp'

    def ready(self):
        import playersapp.signals  # noqa
