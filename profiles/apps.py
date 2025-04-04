# profiles/apps.py
from django.apps import AppConfig

class ProfilesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'profiles'

    # Bu metodu ekliyoruz/override ediyoruz:
    def ready(self):
        import profiles.signals # signals.py dosyasını import et