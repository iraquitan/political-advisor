from django.apps import AppConfig


class PoliticalAdvisorAppConfig(AppConfig):
    name = 'political_advisor'
    verbose_name = 'Political Advisor'

    def ready(self):
        # Registering signals
        from . import signals
