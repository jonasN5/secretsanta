from django.apps import AppConfig


class DrawConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'draw'

    def ready(self):
        # Implicitly connect signal handlers decorated with @receiver.
        from . import signals
