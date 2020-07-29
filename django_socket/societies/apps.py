from django.apps import AppConfig


class SocietiesConfig(AppConfig):
    name = 'societies'

    def ready(self):
        import societies.signals
