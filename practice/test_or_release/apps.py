from django.apps import AppConfig


class TestOrReleaseConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'test_or_release'
