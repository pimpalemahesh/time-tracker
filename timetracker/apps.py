from django.apps import AppConfig


class TimetrackerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'timetracker'

    def ready(self):
        import timetracker.templatetags.timetracker_filters
